# Openarmx与Isacc sim联动

# 一、安装isaacsim

## 1\.下载所需要的文件

https://docs\.isaacsim\.omniverse\.nvidia\.com/5\.0\.0/installation/download\.html

进入链接中下载如下所示文件

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YTMwYzBlMGU2ZGVkNzM0MzYyYTUwZTgyMGMyZTk5ODRfNzA5OTdiZWViMzk0MGNjZTg5MTc0NDMxMWYwNDg4MDFfSUQ6NzYzNDAwOTcxMjQxNzQ0Mjc0OF8xNzgwNDU1MTg5OjE3ODA1NDE1ODlfVjM)

下载Isaacsim本身的压缩包。

## 2\.解压文件

在主目录（home）新建新建文件夹isaac\_sim。

将下载好的压缩包，解压放入到文件夹isaac\_sim中。



进入isaacsim文件夹，打开终端后输入：

```Plain Text
cd ~/isaac_sim
./isaac-sim.selector.sh
```

看到如下界面则表示下载成功

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YWNkZDgwMGI2MDYyMDYzMTU1YTNmNmVjYjc3MjE3YmNfMTVkMjI1ODA2NmQzYzk2NmE4ZjRlMzg0MjU4MDBkNDVfSUQ6NzYzNDAxMDUyNzE2OTY0NTc2M18xNzgwNDU1MTg5OjE3ODA1NDE1ODlfVjM)

# 二、ROS2启动Isaac Sim

NVIDIA官方提供了ROS包，https://github\.com/isaac\-sim/IsaacSim

目前包放入openarmx\_ws中，需要修改以下两个目录。

`文件openarmx_ws/src/isaacsim/scripts/run_isaacsim.py`

修改第一步装的isaacsim的文件夹目录。

```Plain Text
"isaac_sim_path": "/home/huatec/isaac_sim",
```

gui为isaacsim启动时的usd文件路径。

`文件openarmx_ws/src/isaacsim/launch/run_isaacsim.launch.py`

```Plain Text
DeclareLaunchArgument('gui', default_value='/home/huatec/openarmx_ws/openarmx_isaac_urdf/openarmx_isaac.usd', description='Provide the path to a usd file to open it when starting Isaac Sim in standard gui mode. If left empty, Isaac Sim will open an empty stage in standard gui mode.'),
```

# 三、Isaac Lab安装

https://blog\.csdn\.net/m0\_65805744/article/details/150344985

# 四、action graph（ROS通讯）

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=OTg3NWZlODRlODQ3NzUzNDY1MjA2MWNhNGM1Mzc0YWZfZmVmMWYyMTkxZDYyMWViNGIxNTlkMDBlMGU3MzRiYzhfSUQ6NzY0MDAxNDM2Nzg0NTY5ODQ5MV8xNzgwNDU1MTg5OjE3ODA1NDE1ODlfVjM)

注：如果搜不到topic消息，需要查看ROS的domain id是否正确，本项目为66。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ODQ4YWU4M2Q1ZmJiYWQyNzE2YjZiZjdkNzFhNjdiYzZfZjFhMjMyZTFjNzkyZjM1NDEwZTk5NmIzYjA2MWQzNzVfSUQ6NzY0MTQwNDEzMTExMDQ3MjY1M18xNzgwNDU1MTg5OjE3ODA1NDE1ODlfVjM)

如果发布订阅有问题，需要对opeanrmx的根节点进行处理（重置根节点，使isaacsim识别到机器人的各关节）：

选中root\_joint,删除其中的Articulation Root。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ODc4MGYyMDA5Njk2NzRiYjQwMWFiMDY0MGVmZjRlYjBfNTY5NjAyNDEzOTI2ZjIxZDhmMDY1ZjM2NmM3YjJhZGNfSUQ6NzY0MTQwNDg0ODUxMjMyMjUxMF8xNzgwNDU1MTg5OjE3ODA1NDE1ODlfVjM)

右键openarmx，依次点击add，Physics，Articulation Root。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YzQ3NzZmMDU5NzRjMjY3NGRjYjY0M2M5Njc1NTk4M2VfMTdkMjllMjAwMTRlYTQzOGY2NmZjMTgzMGYyODRkYWNfSUQ6NzY0MTQwNTI5OTgyMzkyMjEyNF8xNzgwNDU1MTg5OjE3ODA1NDE1ODlfVjM)

更改完之后，需要关掉self collision enabled，否则机器人会自己碰撞，发生抖动。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=OGI3NzY4ZjliMjc1MTRlMDdjNGM2MDllODJkODJiYTdfNmE1MWYzYjA5YmU5OTgzOTUzMDhkYzlmNGZiZDZiOWRfSUQ6NzY0MTQwNTk0MjcxODEwNjU3N18xNzgwNDU1MTg5OjE3ODA1NDE1ODlfVjM)

# 五、Isaac Sim中使用lerobot录制数据集

## 终端 1：启动 Isaac Sim

```Plain Text
cd ~/openarmx_ws 
source install/setup.bash

ros2 launch isaacsim run_isaacsim.launch.py
```

## 终端 2：启动 OpenArmX 双臂控制（现在默认为抬手姿态）

```Plain Text
cd ~/openarmx_ws
source install/setup.bash

ros2 launch isaacsim openarmx_command_to_joint_state.launch.py 
```

## 终端 3：启动 PICO VR 手柄

```Plain Text
cd ~/openarmx_ws
source install/setup.bash

ros2 launch openarmx_teleop_vr_pico teleop_vr_pico.launch.py
```

## 终端 4：启动 VR 到 OpenArmX 桥接节点

```Plain Text
cd ~/openarmx_ws
source install/setup.bash

ros2 run openarmx_teleop_bridge_vr_pico openarmx_teleop_bridge_vr_pico_node
```

## 终端 5：启动 LeRobot 录数据

```Plain Text
lerobot-env
HF_HUB_OFFLINE=1 lerobot-record \
      --robot.type=openarmx_follower_ros2 \
      --teleop.type=openarmx_leader_ros2 \
      --dataset.repo_id=local/openarmx_dataset \
      --dataset.single_task="palce the green cube on the box" \
      --dataset.num_episodes=50 \
      --dataset.episode_time_s=9999 \
      --dataset.reset_time_s=15 \
      --dataset.push_to_hub=false \
      --display_data=true \
      --dataset.vcodec=h264
      # 编码器名称['h264', 'hevc', 'libsvtav1']
```

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YTU2N2ZiNmFiMmY1ZWFhZDY4ZDI2NTIxNjA1NGUyZTRfNzJlYTNkODJjZWJjOTYxY2VkMGZhM2U3ZTk5MzZjMTFfSUQ6NzYzNDA1NjI1NzQ4OTUzODAwN18xNzgwNDU1MTg5OjE3ODA1NDE1ODlfVjM)



export ISAACSIM\_PATH="$\{HOME\}/isaac\_sim"

export ISAACSIM\_PYTHON\_EXE="$\{ISAACSIM\_PATH\}/python\.sh"

# 六、Isaac Lab中使用lerobot录制数据集

## 启动 Isaac Lab

```Plain Text
cd ~/isaac_lab
conda activate env_isaaclab

./isaaclab.sh -p my_env/demo.py 

```

# 七、重力补偿实体对仿真同构遥操

## **7\.1先生成 urdf 文件**

执行指令：

```Plain Text
cd ~/opeanrmx_ws
xacro ./src/openarmx_description/urdf/robot/v10.urdf.xacro  arm_type:=v10 bimanual:=true > /tmp/v10_bimanual.urdf
```

## **7\.2启动双臂**

```Bash
source ~/openarmx_ws/install/setup.bash
ros2 launch openarmx_teleop_bimanual teleop_bimanual_with_gravitycomp.launch.py
```

\[file\_v3\_0011n\_f1fb9788\-2784\-4349\-a6ef\-7560765356fg\.mp4\]

# 八、Isaac常见问题

## 8\.1点击 Extensions 崩溃或aciton graph消失

问题现象：启动 Isaac Sim 时日志报错：

```Plain Text
omni.kit.converter.hoops failed to load
```

后续点击：

```Plain Text
Window -> Extensions
```

会直接崩溃。

日志里真正关键报错是：

```Plain Text
ModuleNotFoundError: No module named 'psutil'
```

说明 **Isaac Sim 自带 Python 环境缺少 ****`psutil`**** 包**。

Extensions 窗口在扫描扩展时，会加载部分扩展测试模块，这些模块依赖 `psutil`，缺少该库后导致 Extensions 界面崩溃。

解决方法用 Isaac Sim 自带的 `python.sh` 安装：

```Plain Text
cd ~/isaac_sim
./python.sh -m pip install --upgrade pip
./python.sh -m pip install psutil
```

验证是否安装成功：

```Plain Text
./python.sh -c "import psutil; print(psutil.__version__)"
```

能正常输出版本号即可。

## 8\.2 如何关闭线框显示

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NGU1NzQ3Y2RmOTgzMGY5OWFhZDcwNzE0MjljNzZjY2JfODljYTcyODI2MTM3NDcyYmE2MDI2Mzc3MzU5ZjYyMTBfSUQ6NzYzOTI2NDYxMjcwMTQyNDg1OF8xNzgwNDU1MTg5OjE3ODA1NDE1ODlfVjM)

左上角菜单里这一项：

```Plain Text
Wireframe    快捷键Shift + W
```

## 8\.3夹爪碰撞体积修改

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MGU1ODlhY2ZjNTE4MDdjNDc3MGNmZDQxOTk5YmZmZThfYjc2NTU1ZTkzYTBiNWI5NjUxMjlmOThmNmNhNWZiMDFfSUQ6NzY0MDAxMDQ1MzU3NTE1ODc0M18xNzgwNDU1MTg5OjE3ODA1NDE1ODlfVjM)

左边有蓝色标记，说明现在开启了线框显示，所以所有物体都变成白色线框/透明效果。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NTMwNDRkNTlkMDEyODU0MmRlNjQwODM2MTM0Yjg5ZDdfNmVjYmIxMjE5YTM5YTM1MjRkYzQyMjJiNTJmYjllYmZfSUQ6NzYzODkwNzAwMjM2MDA4OTUzMV8xNzgwNDU1MTg5OjE3ODA1NDE1ODlfVjM)

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MWNiMDQyZmZmZTE5OWE3MThmOWE5ZGRjN2Y1YzZlMTdfY2RjNGYzN2FiYjUyNDU4MTIzY2E3MzRhMWI3NTY5NWJfSUQ6NzYzODkzMjU0NzkwODkxNDM1N18xNzgwNDU1MTg5OjE3ODA1NDE1ODlfVjM)



## 8\.4摩擦力绑定

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NDEyOWExYjM4NTJkMjY1NTMxMDhkYjdkZjZlYzU2NjlfNGNiNmM2OGEwNjgwNTliMDI5N2EwMjk3MTBkMGQxODJfSUQ6NzYzOTI2NzkyNjYwMDQ1MzA1MF8xNzgwNDU1MTg5OjE3ODA1NDE1ODlfVjM)

## 8\.5 输出力矩

机械臂抖动现象：

\[录屏 2026年05月14日 09时24分44秒\.webm\]



在 Isaac Sim 这个 Joint Drive 里，基本就是用类似 PD 的方式让关节追踪目标位置和目标速度：

```Plain Text
输出力矩 ≈ Kp（Stiffness） × 位置误差 + Kd × 速度误差（Damping）
```

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YmMyNDc2MjMxNzY0ODg1M2VlZWJlNGRjYzI3MmIwOTFfZTkzZTM3MzYxNDIyODEzOGJiZmJiMTkyMTc2MDIyZTlfSUQ6NzYzOTI2OTg4MTgxNDk3NzcxNl8xNzgwNDU1MTg5OjE3ODA1NDE1ODlfVjM)

设定完Max force、Damping、stiffness之后，可以看见抓起来物体，但是存在一些穿模问题。

\[录屏 2026年05月13日 15时35分12秒\.webm\]

\[录屏 2026年05月15日 14时50分59秒\.webm\]





# 九、Isaac Lab Mimic数据合成

https://isaac\-sim\.github\.io/IsaacLab/main/source/overview/imitation\-learning/teleop\_imitation\.html

## 9\.1 数据采集

```Plain Text
cd ~/isaac_lab
conda activate env_isaaclab
./isaaclab.sh -p my_env/record_demo.py --passive --episodes 10
```

## 9\.2 数据合成

原理：基于少量人工示教轨迹自动扩增高质量任务数据。

首先通过人工遥操作采集若干条成功的抓取放置轨迹，并保存为 HDF5 格式；随后对原始轨迹进行子任务标注，将完整任务划分为接近物体、下降抓取、夹爪闭合、抬升、移动到目标位置和释放物体等阶段。数据生成阶段，Mimic 根据随机化后的物体位姿，对原始示教中的末端执行器轨迹进行空间变换，并通过插值方式拼接不同子任务片段，形成新的候选轨迹。候选轨迹会在 Isaac Lab 仿真环境中重新执行，并根据任务成功判据筛选，只有成功完成抓取放置任务的 episode 才会被写入最终数据集。最终生成的 HDF5 数据再转换为 LeRobotDataset 格式，用于 SmolVLA 策略训练。

```Bash
cd ~/isaac_lab
conda activate env_isaaclab
# 第 1 步：重新标注（过滤不完整 episode）
./isaaclab.sh -p my_env/annotate_demos.py \
    --input ./datasets/cube_tray_source.hdf5 \
    --output ./datasets/cube_tray_annotated.hdf5

# 第 2 步：重新运行数据生成
cd ~/isaac_lab
conda activate env_isaaclab
./isaaclab.sh -p my_env/generate_mimic_dataset.py \
    --input_file ./datasets/cube_tray_annotated.hdf5 \
    --output_file ./datasets/cube_tray_generated.hdf5 \
    --generation_num_trials 50 \
    --enable_cameras
    
```

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NWQ2NTgxZDE5Nzg4OGVmNjNhZmFkZDk4MDM1NjYzODhfMmNlZThiYjU1ZDViODc4YzkyNGI2MjJkYWQ3NDU4N2VfSUQ6NzY0MTkwMzgzMTQyODcxMzY5Nl8xNzgwNDU1MTg5OjE3ODA1NDE1ODlfVjM)



\[录屏 2026年05月22日 10时21分58秒\.webm\]

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZmFhMDAyNzVlZTk1MzcyNGQ5MzBhMjUzODMwZjY2MmFfZDc0MzgzNzI2NDcxMDI3N2QyYzQzYTIwM2Q1ODgxNjdfSUQ6NzY0MjYyOTc3MTQzNjM2Mjk0OF8xNzgwNDU1MTg5OjE3ODA1NDE1ODlfVjM)



![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MDdlNTA2ZmZlYzlkYmVkNzQyYmQyNGViYjc1MDc4YTBfOGQ5MWE1YWRjMGUwM2ZjOTBlNTA1MzBjMjEzMDUyOThfSUQ6NzY0MjIwODEzMDkzOTcwMjIzMV8xNzgwNDU1MTg5OjE3ODA1NDE1ODlfVjM)

数据生成完之后，对hdf5格式转换成lerbotdataset格式。

```Plain Text
cd ~/isaac_lab
python3 /home/huatec/isaac_lab/my_env/convert_to_lerobot.py
```

## 9\.3 数据查看（lerbot格式）

```Plain Text
lerobot-env
HF_HUB_OFFLINE=1 lerobot-dataset-viz \
  --repo-id local/openarmx_dataset \
  --root /home/huatec/isaac_lab/datasets/cube_tray_lerobot_finger_action \
  --mode local \
  --episode-index 0 \
  --display-compressed-images false
```

## 9\.4 训练（smolvla）

```Plain Text
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890
export all_proxy=socks5://127.0.0.1:7890

lerobot-env
lerobot-train \
  --dataset.repo_id=local/openarmx_dataset \
  --dataset.root=/home/huatec/isaac_lab/datasets/cube_tray_lerobot \
  --dataset.video_backend=pyav \
  --policy.type=smolvla \
  --policy.pretrained_path=/home/huatec/models/smolvla_base \
  --policy.vlm_model_name=/home/huatec/models/SmolVLM2-500M-Video-Instruct \
  --policy.push_to_hub=false \
  --batch_size=16 \
  --steps=30000 \
  --output_dir=/home/huatec/isaac_lab/smolvla_output_fit_unfreeze \
  --wandb.enable=true \
  --log_freq=50 \
  --save_freq=5000
```



```Plain Text
lerobot-env
lerobot-train \
  --dataset.repo_id=local/openarmx_dataset \
  --dataset.root=/home/huatec/isaac_lab/datasets/cube_tray_lerobot \
  --dataset.video_backend=pyav \
  --dataset.image_transforms.enable=true \
  --policy.type=smolvla \
  --policy.pretrained_path=/home/huatec/models/smolvla_base \
  --policy.vlm_model_name=/home/huatec/models/SmolVLM2-500M-Video-Instruct \
  --policy.push_to_hub=false \
  --batch_size=1 \
  --steps=30000 \
  --output_dir=/home/huatec/isaac_lab/smolvla_output_fit_unfreeze \
  --wandb.enable=true \
  --policy.train_expert_only=false \
  --policy.freeze_vision_encoder=false \
  --log_freq=50 \
  --save_freq=5000

```



断点训练：

```Plain Text
lerobot-env

lerobot-train \
  --config_path=/home/huatec/isaac_lab/smolvla_output_fit/checkpoints/030000/pretrained_model/train_config.json \
  --resume=true \
  --steps=60000 \
  --output_dir=/home/huatec/isaac_lab/smolvla_output_fit \
  --wandb.enable=true \
  --log_freq=50 \
  --save_freq=5000
```



\[录屏 2026年05月29日 09时32分03秒\.webm\]

## 9\.5 推理

```Plain Text
lerobot-env

HF_HUB_OFFLINE=1 lerobot-record \
  --robot.type=openarmx_follower_ros2 \
  --robot.skip_send_action=false \
  --dataset.repo_id=local/eval_smolvla_openarmx_output \
  --dataset.single_task="place the green cube on the box" \
  --dataset.num_episodes=100 \
  --dataset.episode_time_s=999 \
  --dataset.reset_time_s=10 \
  --dataset.push_to_hub=false \
  --display_data=true \
  --policy.type=smolvla \
  --policy.pretrained_path="/home/huatec/isaac_lab/smolvla_output_fit/checkpoints/050000/pretrained_model" \
  --policy.device=cuda

```

没对夹爪进行平滑处理，导致模型学习到夹爪一直开关闭合。

\[录屏 2026年05月29日 14时26分48秒\.webm\]

对夹爪的action进行平滑处理之后，夹爪明显不再反复开关。

\[录屏 2026年06月01日 08时47分45秒\.webm\]



