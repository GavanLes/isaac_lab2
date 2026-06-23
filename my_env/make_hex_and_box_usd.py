"""
One-shot script to generate standalone USD files:
  - hex_prism.usd   (dark green hexagonal prism, side=2.5cm, height=4.5cm)
  - blue_box.usd    (blue open-top box, 30x20x8cm, wall thickness 1cm)
"""
import math
from pxr import Gf, PhysxSchema, Sdf, UsdGeom, UsdPhysics, UsdShade

USD_DIR = "/home/huatec/isaac_lab/my_env"

# ============================================================
# Hexagonal Prism
# ============================================================
def make_hex_prism():
    side = 0.025   # 2.5cm
    height = 0.045  # 4.5cm
    R = side
    hz = height * 0.5
    angles = [math.radians(a) for a in (0, 60, 120, 180, 240, 300)]

    top_pts = [Gf.Vec3f(R * math.cos(a), R * math.sin(a), hz) for a in angles]
    bot_pts = [Gf.Vec3f(R * math.cos(a), R * math.sin(a), -hz) for a in angles]
    top_center = Gf.Vec3f(0, 0, hz)
    bot_center = Gf.Vec3f(0, 0, -hz)
    points = top_pts + bot_pts + [top_center, bot_center]

    face_vertex_counts = []
    face_vertex_indices = []

    # Top cap: 6 triangle fans
    for i in range(6):
        face_vertex_counts.append(3)
        face_vertex_indices.extend([12, i, (i + 1) % 6])
    # Bottom cap: 6 reversed triangles
    for i in range(6):
        face_vertex_counts.append(3)
        face_vertex_indices.extend([13, 6 + (i + 1) % 6, 6 + i])
    # Side quads
    for i in range(6):
        j = (i + 1) % 6
        face_vertex_counts.append(4)
        face_vertex_indices.extend([i, j, 6 + j, 6 + i])

    stage_path = f"{USD_DIR}/hex_prism.usd"
    stage = Usd.Stage.CreateNew(stage_path)

    mesh = UsdGeom.Mesh.Define(stage, "/HexPrism")
    mesh.CreatePointsAttr(points)
    mesh.CreateFaceVertexCountsAttr(face_vertex_counts)
    mesh.CreateFaceVertexIndicesAttr(face_vertex_indices)
    mesh.CreateDisplayColorAttr([Gf.Vec3f(0.0, 0.35, 0.0)])

    prim = mesh.GetPrim()
    UsdPhysics.CollisionAPI.Apply(prim)

    rigid_api = UsdPhysics.RigidBodyAPI.Apply(prim)
    rigid_api.CreateRigidBodyEnabledAttr(True)
    rigid_api.CreateKinematicEnabledAttr(False)

    mass_api = UsdPhysics.MassAPI.Apply(prim)
    mass_api.CreateMassAttr(0.05)

    # Dark green material, high friction
    mat = UsdShade.Material.Define(stage, "/HexPrism/Looks/DarkGreenMat")
    shader = UsdShade.Shader.Define(stage, "/HexPrism/Looks/DarkGreenMat/PreviewSurface")
    shader.CreateIdAttr("UsdPreviewSurface")
    shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(0.0, 0.35, 0.0))
    shader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.45)
    shader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)
    mat.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), "surface")

    phys_api = UsdPhysics.MaterialAPI.Apply(mat.GetPrim())
    phys_api.CreateStaticFrictionAttr(20.0)
    phys_api.CreateDynamicFrictionAttr(20.0)
    phys_api.CreateRestitutionAttr(0.0)
    px_api = PhysxSchema.PhysxMaterialAPI.Apply(mat.GetPrim())
    px_api.CreateFrictionCombineModeAttr("max")

    UsdShade.MaterialBindingAPI(prim).Bind(mat)
    stage.GetRootLayer().Save()
    print(f"Created: {stage_path}")


# ============================================================
# Blue Open-Top Box (30x20x8 cm, wall/base thickness 1cm)
# ============================================================
def make_box_part(stage, path, pos, scale, mat):
    cube = UsdGeom.Cube.Define(stage, path)
    cube.CreateSizeAttr(1.0)
    cube.CreateDisplayColorAttr([Gf.Vec3f(0.1, 0.2, 0.7)])
    prim = cube.GetPrim()
    xform = UsdGeom.Xformable(prim)
    xform.ClearXformOpOrder()
    xform.AddTranslateOp().Set(pos)
    xform.AddScaleOp().Set(scale)
    UsdShade.MaterialBindingAPI(prim).Bind(mat)
    UsdPhysics.CollisionAPI.Apply(prim)
    return prim


def make_blue_box():
    size_x = 0.30    # 30cm
    size_y = 0.20    # 20cm
    wall_thick = 0.01  # 1cm
    base_thick = 0.01  # 1cm
    wall_h = 0.08      # 8cm

    base_z = 0.0
    wall_z = (base_thick + wall_h) * 0.5

    wall_x_len = size_x + wall_thick * 2.0
    wall_y_len = size_y

    stage_path = f"{USD_DIR}/blue_box.usd"
    stage = Usd.Stage.CreateNew(stage_path)

    # Blue material
    mat = UsdShade.Material.Define(stage, "/Box/Looks/BlueMat")
    shader = UsdShade.Shader.Define(stage, "/Box/Looks/BlueMat/PreviewSurface")
    shader.CreateIdAttr("UsdPreviewSurface")
    shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(0.1, 0.2, 0.7))
    shader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.5)
    shader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)
    mat.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), "surface")

    phys_api = UsdPhysics.MaterialAPI.Apply(mat.GetPrim())
    phys_api.CreateStaticFrictionAttr(0.8)
    phys_api.CreateDynamicFrictionAttr(0.6)
    phys_api.CreateRestitutionAttr(0.0)

    # Kinematic rigid body on root Xform
    root = UsdGeom.Xform.Define(stage, "/BlueBox")
    root_prim = root.GetPrim()
    rigid_api = UsdPhysics.RigidBodyAPI.Apply(root_prim)
    rigid_api.CreateRigidBodyEnabledAttr(True)
    rigid_api.CreateKinematicEnabledAttr(True)

    # Base
    make_box_part(stage, "/BlueBox/Base",
                  Gf.Vec3d(0.0, 0.0, base_z),
                  Gf.Vec3f(size_x, size_y, base_thick), mat)

    # Walls: +Y, -Y, +X, -X
    make_box_part(stage, "/BlueBox/Wall_PosY",
                  Gf.Vec3d(0.0, size_y * 0.5 + wall_thick * 0.5, wall_z),
                  Gf.Vec3f(wall_x_len, wall_thick, wall_h), mat)
    make_box_part(stage, "/BlueBox/Wall_NegY",
                  Gf.Vec3d(0.0, -size_y * 0.5 - wall_thick * 0.5, wall_z),
                  Gf.Vec3f(wall_x_len, wall_thick, wall_h), mat)
    make_box_part(stage, "/BlueBox/Wall_PosX",
                  Gf.Vec3d(size_x * 0.5 + wall_thick * 0.5, 0.0, wall_z),
                  Gf.Vec3f(wall_thick, wall_y_len, wall_h), mat)
    make_box_part(stage, "/BlueBox/Wall_NegX",
                  Gf.Vec3d(-size_x * 0.5 - wall_thick * 0.5, 0.0, wall_z),
                  Gf.Vec3f(wall_thick, wall_y_len, wall_h), mat)

    stage.GetRootLayer().Save()
    print(f"Created: {stage_path}")


if __name__ == "__main__":
    make_hex_prism()
    make_blue_box()
