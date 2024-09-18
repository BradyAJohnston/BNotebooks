import bpy

from . import installer, pkg


def button_install_pkg(layout, name, version, desc=""):
    layout = layout.row()
    if pkg.is_available(name, version):
        row = layout.row()
        row.label(text=f"{name} version {version} is installed.")
        op = row.operator("mol.install_package", text=f"Reinstall {name}")
        op.package = name
        op.version = version
        op.description = f"Reinstall {name}"
    else:
        row = layout.row(heading=f"Package: {name}")
        col = row.column()
        col.label(text=str(desc))
        col = row.column()
        op = col.operator("mol.install_package", text=f"Install {name}")
        op.package = name
        op.version = version
        op.description = f"Install required python package: {name}"


class BNotebooksPreferences(bpy.types.AddonPreferences):
    bl_idname = "BNotebooks"

    overwrite: bpy.props.BoolProperty(
        name="Overwrite?",
        description="If a kernal of this name already exists, overwrite it",
        default=True
    )
    name: bpy.props.StringProperty(
        name="Name",
        description="Name that will appear in the Jupyter kernal list",
        default=f"blender_{bpy.app.version_string}"
    )

    def draw(self, context):
        layout = self.layout
        col = layout.column(heading="", align=False)
        col.label(text="Install required python packages.")
        for package in pkg.get_pkgs().values():
            button_install_pkg(col, package.get("name"), version=package.get(
                "version"), desc=package["desc"])
        col.label(text="Manage kernel registration.")
        row = layout.row()
        row.prop(self, "name")
        row.prop(self, "overwrite")
        op = row.operator("bn.kernel_append")
        op.overwrite = self.overwrite
        op.name = self.name
        op = row.operator("bn.kernel_remove")
        op.name = self.name


class BN_Kernel_Append(bpy.types.Operator):
    bl_idname = "bn.kernel_append"
    bl_label = "Append Kernel"
    bl_description = "Append this blender's python as a jupyter kernel."
    bl_options = {"REGISTER"}

    overwrite: bpy.props.BoolProperty(
        name="overwrite",
        default=True
    )

    name: bpy.props.StringProperty(
        name="Kernel Name",
        description="Name for the kernel",
        default="Blender"
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        installer.install(
            blender_exec=bpy.app.binary_path,
            kernel_name=self.name,
            overwrite=self.overwrite
        )
        return {"FINISHED"}


class BN_Kernel_Remove(bpy.types.Operator):
    bl_idname = "bn.kernel_remove"
    bl_label = "Remove Kernel"
    bl_description = "Append this blender's python as a jupyter kernel."
    bl_options = {"REGISTER"}

    # overwrite: bpy.props.BoolProperty(
    #     name = "overwrite",
    #     default = True
    # )

    name: bpy.props.StringProperty(
        name="Kernel Name",
        description="Name for the kernel",
        default="Blender"
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        installer.remove(
            kernel_name=self.name
        )
        return {"FINISHED"}
