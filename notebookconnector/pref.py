import bpy

from . import installer, __package__


class NotebookConnectorPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    overwrite: bpy.props.BoolProperty(  # type: ignore
        name="Overwrite?",
        description="If a kernal of this name already exists, overwrite it",
        default=True,
    )
    name: bpy.props.StringProperty(  # type: ignore
        name="Name",
        description="Name that will appear in the Jupyter kernal list",
        default=f"blender_{bpy.app.version_string.replace(' ', '_')}",
    )

    def draw(self, context):
        layout = self.layout

        layout.label(text="Manage kernel registration.")
        row = layout.row()
        row.prop(self, "name")
        row.prop(self, "overwrite")
        row = layout.row()
        op = row.operator("bn.kernel_append")
        op.overwrite = self.overwrite
        op.name = self.name
        op = row.operator("bn.kernel_remove")
        op.name = self.name


class NC_Kernel_Append(bpy.types.Operator):
    bl_idname = "bn.kernel_append"
    bl_label = "Append Kernel"
    bl_description = "Append this blender's python as a jupyter kernel."
    bl_options = {"REGISTER"}

    overwrite: bpy.props.BoolProperty(  # type: ignore
        name="overwrite", default=True
    )

    name: bpy.props.StringProperty(  # type: ignore
        name="Kernel Name", description="Name for the kernel", default="Blender"
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        try:
            installer.install(kernel_name=self.name, overwrite=self.overwrite)
        except ValueError:
            self.report(
                {"ERROR"},
                "Kernel name cannot contain spaces!",
            )
            return {"CANCELLED"}
        return {"FINISHED"}


class NC_Kernel_Remove(bpy.types.Operator):
    bl_idname = "bn.kernel_remove"
    bl_label = "Remove Kernel"
    bl_description = "Append this blender's python as a jupyter kernel."
    bl_options = {"REGISTER"}

    name: bpy.props.StringProperty(  # type: ignore
        name="Kernel Name", description="Name for the kernel", default="Blender"
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        installer.remove(kernel_name=self.name)
        return {"FINISHED"}


CLASSES = (NotebookConnectorPreferences, NC_Kernel_Append, NC_Kernel_Remove)
