import bpy
import random

# to duplicate an object
def duplicate(obj, data=True, actions=True, collection=None):
    obj_copy = obj.copy()
    if data:
        obj_copy.data = obj_copy.data.copy()
    if actions and obj_copy.animation_data:
        obj_copy.animation_data.action = obj_copy.animation_data.action.copy()
    collection.objects.link(obj_copy)
    return obj_copy
# convert a hex value to rgb
def rgb( hex_value ):
    b = (hex_value & 0xFF) / 255.0
    g = ((hex_value >> 8) & 0xFF) / 255.0
    r = ((hex_value >> 16) & 0xFF) / 255.0
    return r, g, b, 1
# random int between start and end values
def ran(start,end):
    return random.randint(start, end)
# random float between start and end values
def ranfloat(start,end):
    return random.uniform(start,end)
# remove all selected objects in scene
def deleteAllObjects():

    for mesh in bpy.context.selected_objects:
        # Delete the meshes
        if(mesh.name != 'Camera'):
            bpy.data.objects.remove( mesh )
# returns a random rbg color
def get_random_color(mode = False):
    cols = [0x636d73, 0x99a09d, 0x889395, 0x33393a, 0xafb9b8, 0x3c4044, 0x7f8788, 0xcdd3d3, 0xaab5a9,0x3b4e45,0x4d5859, 0x495749]
    if(not mode):
        return rgb(cols[ran(0,11)])
    else:
        return cols[ran(0,11)]
