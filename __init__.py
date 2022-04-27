bl_info = {
    "name": "CityMaker",
    "author": "seeward",
    "version": (1, 0),
    "blender": (3, 1, 0),
    "location": "View3D > Add > Mesh > Generative City",
    "description": "Adds a new City of Mesh Objects",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}


import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper
import random
from math import radians


# todo add city config properties to the panel
class CityPanel(bpy.types.Panel):
    bl_label = "Config City"
    bl_idname = "InstaCity"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "CityMaker"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("mesh.add_city")
        row = layout.row()
        row.label(text="Configure the City", icon = "CUBE")
        
        

space = 3
block_space = .5

def duplicate(obj, data=True, actions=True, collection=None):
    obj_copy = obj.copy()
    if data:
        obj_copy.data = obj_copy.data.copy()
    if actions and obj_copy.animation_data:
        obj_copy.animation_data.action = obj_copy.animation_data.action.copy()
    collection.objects.link(obj_copy)
    return obj_copy

def rgb( hex_value ):
    b = (hex_value & 0xFF) / 255.0
    g = ((hex_value >> 8) & 0xFF) / 255.0
    r = ((hex_value >> 16) & 0xFF) / 255.0
    return r, g, b, 1

def ran(start,end):
    return random.randint(start, end)

def ranfloat(start,end):
    return random.uniform(start,end)

def deleteAllObjects():

    for mesh in bpy.context.selected_objects:
        # Delete the meshes
        bpy.data.objects.remove( mesh )

def get_random_color():
    ''' generate rgb using a list comprehension '''
    r, g, b = [ran(0,5) for i in range(3)]
    return r, g, b, 1

class OBJECT_OT_add_city(Operator, AddObjectHelper):
    """Create a new Generative Coty"""
    bl_idname = "mesh.add_city"
    bl_label = "Mesh City"
    bl_options = {'REGISTER', 'UNDO'}
    city_blocks: bpy.props.IntProperty(name="CityBlocks", default=3, min=1, max=10)
    building_max_h: bpy.props.IntProperty(name="MaxHeight", default=4, min=1, max=7)
    use_colors: bpy.props.BoolProperty(name="UseColors", default=True)    
    use_trees: bpy.props.BoolProperty(name="UseTress", default=False)

    scale: FloatVectorProperty(
        name="scale",
        default=(1.0, 1.0, 1.0),
        subtype='TRANSLATION',
        description="scaling",
    )

    def execute(self, context):
        deleteAllObjects()

        # ? bpy.ops.import_scene.fbx(filepath="/Users/seeward/Documents/blender/models/fbx/tree.fbx", global_scale=0.05)
        # ? tree = bpy.context.object

        #  ? add ground
        bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.ops.transform.resize(
            value=(100, 100, 1), 
            orient_type='GLOBAL', 
            orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), 
            orient_matrix_type='GLOBAL', 
            constraint_axis=(True, False, False), 
            mirror=False, use_proportional_edit=False, 
            proportional_edit_falloff='SMOOTH', 
            proportional_size=1, 
            use_proportional_connected=False, 
            use_proportional_projected=False, 
            release_confirm=True)


        for boxX in range(self.city_blocks):
            for boxY in range(self.city_blocks):

                # ? add sidewalks
                bpy.ops.mesh.primitive_cube_add(
                    size=2.5, 
                    enter_editmode=False, 
                    align='WORLD', 
                    location=(boxX * space , boxY * space , 0), 
                    scale=(1, 1, .01))
                # store our locations for each loop
                curX = boxX * space - .5
                curY = boxY * space - .5
                # pick a random block type
                block_type = ran(1,3)
                
                # block split into 1/4s 
                if(block_type == 1):
                    for blockX in range(2):
                        for blockY in range(2):
                            
                            h = ran(0,self.building_max_h) 

                            if(h == 0):
                                h = .05
                           

                            bpy.ops.mesh.primitive_cube_add(
                                size=1, 
                                enter_editmode=False, 
                                align='WORLD', 
                                location=(curX + blockX, curY + blockY , h /2), 
                                scale=(1, 1, h ))

                            if(self.use_colors):
                                color = get_random_color()
                            else:
                                color = rgb(0x717171)

                            obj = bpy.context.object
                            obj.color = color
                            mat = bpy.data.materials.new("Blue")
                            # Activate its nodes
                            mat.use_nodes = True
                            mat.diffuse_color = color
                            # Get the principled BSDF (created by default)
                            principled = mat.node_tree.nodes['Principled BSDF']
                            # Assign the color
                            principled.inputs['Base Color'].default_value = color
                            # Assign the material to the object
                            obj.data.materials.append(mat)
                

                if(block_type == 2):
                    for blockX in range(1):
                        for blockY in range(1):
                            h = ran(0,self.building_max_h) 
                            
                            if(h == 0):
                                h = .05
                           
                            
                                
                            bpy.ops.mesh.primitive_cube_add(
                                size=2, 
                                enter_editmode=False, 
                                align='WORLD', 
                                location=(curX + block_space, curY  + block_space , h/1.0015), 
                                scale=(1, 1, h ))
                                
                            obj = bpy.context.object
                            if(self.use_colors):
                                color = get_random_color()
                            else:
                                color = rgb(0x717171)
                            obj.color = color

                            mat = bpy.data.materials.new("Blue3")

                            # Activate its nodes
                            mat.use_nodes = True

                            # Get the principled BSDF (created by default)
                            principled = mat.node_tree.nodes['Principled BSDF']

                            # Assign the color
                            principled.inputs['Base Color'].default_value = color
                            mat.diffuse_color = color           
                            # Assign the material to the object
                            obj.data.materials.append(mat)

                            if(self.use_trees):
                                bpy.ops.mesh.primitive_cube_add(
                                size=1, 
                                enter_editmode=False, 
                                align='WORLD', 
                                location=(curX + block_space + .25, curY  + block_space + .25 , 0), 
                                scale=(1, 1, 1 ))
                                
                                obj = bpy.context.object
                                subsurf = obj.modifiers.new("myMod", "SUBSURF")
                                subsurf.levels = 3
                        
                
                if(block_type == 3):
                    for blockX in range(2):
                        for blockY in range(2):
                            
                            h = ran(0,self.building_max_h) 

                            if(h == 0):
                                h = .05
                           
                            bpy.ops.mesh.primitive_cube_add(
                                size=1, 
                                enter_editmode=False, 
                                align='WORLD', 
                                location=(curX + blockX, curY + blockY , h/2), 
                                scale=(1, 1, h ))

                            obj = bpy.context.object
                            if(self.use_colors):
                                color = get_random_color()
                            else:
                                color = rgb(0x717171)
                            obj.color = color
                            mat = bpy.data.materials.new("Blue2")

                            # Activate its nodes
                            mat.use_nodes = True

                            # Get the principled BSDF (created by default)
                            principled = mat.node_tree.nodes['Principled BSDF']

                            # Assign the color
                            principled.inputs['Base Color'].default_value = color
                            mat.diffuse_color = color

                            # Assign the material to the object
                            obj.data.materials.append(mat)

        return {'FINISHED'}


# Registration

def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_city.bl_idname,
        text="Add City",
        icon='CUBE')


# This allows you to right click on a button and link to documentation
def add_object_manual_map():
    url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_city", "scene_layout/object/types.html"),
    )
    return url_manual_prefix, url_manual_mapping


def register():
    bpy.utils.register_class(OBJECT_OT_add_city)
    bpy.utils.register_class(CityPanel)
    bpy.utils.register_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_add.append(add_object_button)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_city)
    bpy.utils.unregister_class(CityPanel)
    bpy.utils.unregister_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_add.remove(add_object_button)


if __name__ == "__main__":
    register()
