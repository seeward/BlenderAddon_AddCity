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


from sys import _xoptions
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

def get_random_color(mode = False):
    cols = [0x636d73, 0x99a09d, 0x889395, 0x33393a, 0xafb9b8, 0x3c4044, 0x7f8788, 0xcdd3d3, 0xaab5a9,0x3b4e45,0x4d5859, 0x495749]
    if(not mode):
        return rgb(cols[ran(0,11)])
    else:
        return cols[ran(0,11)]
class OBJECT_OT_add_city(Operator, AddObjectHelper):
    """Create a new Generative Coty"""
    bl_idname = "mesh.add_city"
    bl_label = "Mesh City"
    bl_options = {'REGISTER', 'UNDO'}
    city_blocks: bpy.props.IntProperty(name="CityBlocks", default=3, min=1, max=10)
    building_max_h: bpy.props.IntProperty(name="MaxHeight", default=4, min=1, max=7)
    use_colors: bpy.props.BoolProperty(name="UseColors", default=True)    
    use_trees: bpy.props.BoolProperty(name="UseTress", default=True)
    
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

        obj = bpy.context.object
        self.add_mat(obj,0x5F6975, "ground_0")

        for boxX in range(self.city_blocks):
            for boxY in range(self.city_blocks):

                # ? add sidewalks
                
                obj = self.make_building((boxX * space , boxY * space , 0),2.5,.01)
                self.add_mat(obj,0xc1c1c1, "side_walk")
                # store our locations for each loop
                curX = boxX * space - .5
                curY = boxY * space - .5
                # pick a random block type
                block_type = ran(1,3)
                
                # block split into 1/4s 
                if(block_type == 1 or block_type == 3):
                    for blockX in range(2):
                        for blockY in range(2):
                            h = ran(0,self.building_max_h) 
                            if(h == 0):
                                h = .05
                            if(self.use_colors):
                                color = get_random_color(True)
                            else:
                                color = 0x717171

                            obj = self.make_building((curX + blockX, curY + blockY , h /2),1, h)
                            self.add_mat(obj,color, "blue")
                
                # single large block or garden
                if(block_type == 2):
                    for blockX in range(1):
                        for blockY in range(1):
                            h = ran(0,self.building_max_h) 
                            
                            if(h == 0):
                                h = .05
                                
                            obj = self.make_building((curX + block_space, curY  + block_space , h/1.0015),2, h)
                            if(self.use_colors):
                                color = get_random_color(True)
                            else:
                                color = 0x717171
                            
                            if(h == .05):
                                color = 0x199313
                            
                            self.add_mat(obj, color, "building_1")

                            if(h == .05):
                                r = ran(1,3)
                                if(r == 1):
                                    r = get_random_color(True)
                                    bpy.ops.mesh.primitive_plane_add(
                                        size=1, 
                                        enter_editmode=False, 
                                        align='WORLD', 
                                        location=(curX + block_space, curY  + block_space , .10115), 
                                        scale=(1,2, 1))

                                    bpy.ops.transform.resize(
                                        value=(.5, 2, 1), 
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
                                    obj = bpy.context.object
                                    self.add_mat(obj, r, "concrete_0")
                                    bpy.ops.mesh.primitive_plane_add(
                                        size=1, 
                                        enter_editmode=False, 
                                        align='WORLD', 
                                        location=(curX + block_space, curY  + block_space , .10115), 
                                        scale=(2,1, 1))

                                    bpy.ops.transform.resize(
                                        value=(2, .5, 1), 
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
                                    obj = bpy.context.object
                                    self.add_mat(obj, r, "concrete_1")
                                if(r == 2):
                                    bpy.ops.mesh.primitive_plane_add(
                                        size=1, 
                                        enter_editmode=False, 
                                        align='WORLD', 
                                        location=(curX + block_space, curY  + block_space, .10115), 
                                        scale=(1,1, 1))
                                    obj = bpy.context.object
                                    self.add_mat(obj, get_random_color(True), "concrete_2")
                                if(r == 3):


                                    bpy.ops.mesh.primitive_uv_sphere_add(
                                        radius=1, 
                                        enter_editmode=False, 
                                        align='WORLD', 
                                        location=(curX + block_space, curY  + block_space, .10115), 
                                        scale=(0, 1, 1))
                                    obj = bpy.context.object
                                    obj.rotation_euler = (radians(90), radians(90), 0)
                                    self.add_mat(obj, get_random_color(True), "concrete_3")

                                    

                            if(self.use_trees and h == .05):
                                for x in range(2):
                                   

                                    for y in range(2):
                                        

                                        x2 = ((curX + block_space) - x) + .5
                                        y = ((curY  + block_space) - y) + .5

                                        self.make_tree(x2,y)
                                        
                                      

                        
        return {'FINISHED'}

    def make_building(self, location, size, height):
        bpy.ops.mesh.primitive_cube_add(
            size=size, 
            enter_editmode=False, 
            align='WORLD', 
            location=location, 
            scale=(1, 1, height ))
        return bpy.context.object


    def make_tree(self,x2,y):
       
        bpy.ops.mesh.primitive_cube_add(
            size=.5, 
            enter_editmode=False, 
            align='WORLD', 
            location=(x2,y,.5), 
            scale=(ranfloat(.75,2.5), ranfloat(.75,2.5), ranfloat(.5,1.5))
        )
        obj = bpy.context.object
        # add a sub surface modifier
        subsurf = obj.modifiers.new("myMod", "SUBSURF")
        # randomize the surface
        subsurf.levels = ran(1,5)
        self.add_mat(obj, 0x91C11D, "top_of_tree")
        # make the trunk of the tree
        bpy.ops.mesh.primitive_cylinder_add(
            radius=.1, 
            depth=2, 
            enter_editmode=False, 
            align='WORLD', 
            location=(x2, y, .2), 
            scale=((ranfloat(.1,.5),ranfloat(.1,.5), .2)))

        obj = bpy.context.object
        self.add_mat(obj, 0x936413, "trunk_of_tree")
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=.15, 
            enter_editmode=False, 
            align='WORLD', 
            location=(x2, y, .10115), 
            scale=(0, 1, 1))
        obj = bpy.context.object
        self.add_mat(obj, 0x000000, "base_of_tree")
        obj.rotation_euler = (radians(90), radians(90), 0)

    def add_mat(self,obj, color, name):
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        principled = mat.node_tree.nodes['Principled BSDF']
        principled.inputs['Base Color'].default_value = rgb(color)
        mat.diffuse_color = rgb(color)           # brown
        obj.data.materials.append(mat)



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
