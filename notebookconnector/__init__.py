from bpy.utils import register_class, unregister_class

from . import pref

class_list = pref.CLASSES


def register():
    for c in class_list:
        register_class(c)


def unregister():
    for c in class_list:
        unregister_class(c)
