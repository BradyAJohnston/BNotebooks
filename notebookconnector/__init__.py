import bpy
from bpy.utils import register_class, unregister_class

from . import pkg, pref


bl_info = {
    "name": "BNotebooks",
    "author": "Brady Johnston",
    "version": (0, 0, 5),
    "blender": (3, 5, 0),
    "location": "Blender Preferences -> Add-ons -> BNotebooks",
    "description": "Makes Blender available as a jupyter kernal.",
    "warning": "",
    "wiki_url": "",
    "category": "Development",
    }

class_list = (
    pref.BNotebooksPreferences,
    pref.BN_Kernel_Append,
    pref.BN_Kernel_Remove,
    pkg.MOL_OT_Install_Package
)


def get_mirror_items(scene, context):
    return [(key, key, "") for key in pkg.PYPI_MIRROR.keys()]


def register():
    bpy.types.Scene.pypi_mirror_provider = bpy.props.EnumProperty(
        name="PyPI Mirror Provider",
        description="Select a PyPI mirror to use",
        items=get_mirror_items
    )
    for c in class_list:
        register_class(c)


def unregister():
    del bpy.types.Scene.pypi_mirror_provider
    for c in class_list:
        unregister_class(c)
