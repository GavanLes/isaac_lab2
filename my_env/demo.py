import argparse
import random
import select
import sys
import termios
import tty

from isaaclab.app import AppLauncher

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(line_buffering=True)
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(line_buffering=True)


# ============================================================
# 1. 启动 Isaac Sim / Isaac Lab
# ============================================================

parser = argparse.ArgumentParser(
    description="Load environment, robot, a cube, and a tray target with reset detection."
)
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()

app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

# 启动后再导入 ROS2 bridge extension，避免和 USD 加载冲突
import omni.kit.app

ext_manager = omni.kit.app.get_app().get_extension_manager()
ext_manager.set_extension_enabled_immediate("isaacsim.ros2.bridge", True)


# ============================================================
# 2. AppLauncher 之后再导入 Isaac / USD 相关模块
# ============================================================

import omni.usd
import isaaclab.sim as sim_utils

from scene_config import (
    CAMERA_EYE,
    CAMERA_TARGET,
    CUBE_HEIGHT,
    CUBE_MASS,
    CUBE_PATH,
    CUBE_SIZE,
    EE_PRIM_CANDIDATES,
    ENV_USD,
    LEFT_INIT_JOINTS,
    RESET_COOLDOWN_STEPS,
    RIGHT_INIT_JOINTS,
    ROBOT_PRIM_CANDIDATES,
    ROBOT_USD,
    TRAY_PRIM_CANDIDATES,
    TRAY_SIZE_X,
    TRAY_SIZE_Y,
    TRAY_WALL_HEIGHT,
)
from scene_utils import (
    add_debug_lights,
    add_sublayer,
    check_prims,
    create_dynamic_cube,
    find_first_valid_prim,
    get_prim_world_position,
    print_stage_prims,
    reset_cube,
    set_joint_positions,
)


# ============================================================
# 3. 主程序
# ============================================================

def main():
    sim_cfg = sim_utils.SimulationCfg(
        dt=0.01,
        device="cpu",
        physx=sim_utils.PhysxCfg(
            solve_articulation_contact_last=True,
            enable_ccd=True,
            min_position_iteration_count=32,
            max_position_iteration_count=128,
            min_velocity_iteration_count=1,
            max_velocity_iteration_count=32,
        ),
    )
    sim = sim_utils.SimulationContext(sim_cfg)
    stage = omni.usd.get_context().get_stage()

    print("=" * 80, flush=True)
    print("[DEBUG] ENV_USD      =", ENV_USD, flush=True)
    print("[DEBUG] ROBOT_USD    =", ROBOT_USD, flush=True)
    print("[DEBUG] CUBE_PATH   =", CUBE_PATH, flush=True)
    print("[DEBUG] TRAY_PRIM   =", TRAY_PRIM_CANDIDATES, flush=True)
    print("=" * 80, flush=True)

    add_sublayer(stage, ENV_USD)
    add_sublayer(stage, ROBOT_USD)
    add_debug_lights(stage)

    robot_path = find_first_valid_prim(stage, ROBOT_PRIM_CANDIDATES)
    robot_pos = get_prim_world_position(stage, robot_path)
    print("[INFO] Robot world position:", robot_pos, flush=True)

    ee_path = find_first_valid_prim(stage, EE_PRIM_CANDIDATES)
    print("[INFO] End-effector path:", ee_path, flush=True)

    def hex_start_pos():
        return [
            robot_pos[0] + 0.35 + random.uniform(-0.05, 0.05),
            robot_pos[1] + 0.19 + random.uniform(-0.05, 0.05),
            robot_pos[2] + 0.20,
        ]

    cube_start_pos = hex_start_pos()
    cube_path = create_dynamic_cube(
        stage,
        CUBE_PATH,
        pos=cube_start_pos,
        size=CUBE_SIZE,
        height=CUBE_HEIGHT,
        mass=CUBE_MASS,
    )
    tray_path = find_first_valid_prim(stage, TRAY_PRIM_CANDIDATES)
    tray_center = get_prim_world_position(stage, tray_path)
    print(f"[INFO] Tray path: {tray_path}, center: {tray_center}", flush=True)

    # 设置机械臂初始关节角度
    all_init_joints = {**LEFT_INIT_JOINTS, **RIGHT_INIT_JOINTS}
    set_joint_positions(stage, robot_path, all_init_joints)

    sim.reset()
    sim.set_camera_view(eye=CAMERA_EYE, target=CAMERA_TARGET)

    print("=" * 80, flush=True)
    print("[INFO] All USD files loaded.", flush=True)
    print(f"[INFO] environment:        {ENV_USD}", flush=True)
    print(f"[INFO] robot:              {ROBOT_USD}", flush=True)
    print(f"[INFO] robot path:         {robot_path}", flush=True)
    print(f"[INFO] cube path:      {cube_path}", flush=True)
    print(f"[INFO] cube start pos: {cube_start_pos}", flush=True)
    print(f"[INFO] tray path:          {tray_path}", flush=True)
    print("=" * 80, flush=True)

    check_prims(stage, robot_path, cube_path, tray_path)
    print_stage_prims(stage)

    # ---- 键盘输入 ----
    _old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())

    def key_pressed():
        return select.select([sys.stdin], [], [], 0)[0] != []

    def read_key():
        return sys.stdin.read(1)

    reset_cooldown = 0
    while simulation_app.is_running():
        sim.step()

        if reset_cooldown > 0:
            reset_cooldown -= 1
            # Flush keyboard buffer during cooldown (ignore buffered 'R' presses)
            while key_pressed():
                read_key()
            continue

        # Manual reset on 'R' key
        if key_pressed() and read_key().lower() == "r":
            sim.reset()
            new_pos = hex_start_pos()
            reset_cube(cube_path, new_pos)
            print(f"[INFO] Manual reset (R key) → cube: ({new_pos[0]:.3f}, {new_pos[1]:.3f}, {new_pos[2]:.3f})")
            sim.set_camera_view(eye=CAMERA_EYE, target=CAMERA_TARGET)
            # TODO: 需要通知 bridge 复位指令，待解决 rclpy 导入问题
            reset_cooldown = RESET_COOLDOWN_STEPS
            continue

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, _old_settings)
    simulation_app.close()


if __name__ == "__main__":
    main()
