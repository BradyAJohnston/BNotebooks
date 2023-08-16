bl_info = {
    "name": "BNotebooks",
    "author": "Brady Johnston",
    "version": (0, 0, 1),
    "blender": (3, 5, 0),
    "location": "Blender Preferences -> Add-ons -> BNotebooks",
    "description": "Makes Blender available as a jupyter kernal.",
    "warning": "",
    "wiki_url": "",
    "category": "Development",
    }

from bpy.utils import register_class, unregister_class
from . import pref

class_list = (
    pref.BNotebooksPreferences,
    pref.BN_Kernel_Append,
    pref.BN_Kernel_Remove
)

def register():
    for c in class_list:
        register_class(c)

def unregister():
    for c in class_list:
        unregister_class(c)
