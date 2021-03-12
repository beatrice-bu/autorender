import math
import bpy
import mathutils
import os
import glob
import random
from mathutils import Vector

path_to_hdrs = 'D:\\Programming\\github\\autorender\\hdrs\\'
path_to_output = 'D:/Programming/output'
img_name = 'chair'


def initializeBG():    
    
    C = bpy.context
    world = C.scene.world
    world.use_nodes = True

    global env_node
    env_node = C.scene.world.node_tree.nodes.new("ShaderNodeTexEnvironment")
    
    node_tree = C.scene.world.node_tree 
    node_tree.links.new(env_node.outputs['Color'], node_tree.nodes['Background'].inputs['Color'])
    
    bpy.context.scene.render.film_transparent = False
    
    
    for file in glob.glob(path_to_hdrs + "*.hdr"):
        
        print(f'Loading file : {file}')
        bpy.data.images.load(file)
        
     
    
initializeBG()
img_random = random.randint(0, len(bpy.data.images))
print(img_random)
env_node.image = bpy.data.images[img_random]
print(env_node.image)
    


def autoRenderCycle(cycles: int)


for c in range(cycles):
    x = uniform(-5,5)
    y = uniform(-5,5)
    if (x >= -1.5 and x <= 1.5) and (y >= -1.5 and y <= 1.5):
        z = uniform(3,5)
    else:
        z = uniform(0,5)
    cam.location = Vector((x, y, z))
    
    
    
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.render.image_settings.color_mode ='RGBA'
    bpy.context.scene.render.image_settings.file_format='PNG' 
    bpy.context.scene.render.image_settings.compression = 90

    bpy.context.scene.render.filepath = os.path.join(path_to_output, f'{img_name}-{str(cycle)}.png')
    bpy.ops.render.render(write_still=True)


chair = bpy.data.objects['Chair']
chair.location = Vector((0,0,0.5)

cam = bpy.data.objects['Camera']

bpy.ops.object.select_all(action='DESELECT')


cam.select_set(True)
cam = bpy.context.object

bpy.ops.object.constraint_add(type='TRACK_TO')
bpy.context.object.constraints["Track To"].target = bpy.data.objects["Chair"]
bpy.context.object.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'



class autorenderPanel(bpy.types.Panel):
    bl_label = "Auto Render"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"
    bl_category = "Autorender"
    
    
    def draw(self, context):
        row = self.layout.row()
        row.label(text='Autorendering script')
        column = self.layout.column(align=True)
        column.operator("render.initialize", text="Initialize Environment"
        column.operator("render.autorender", text="Begin AutoRendering")
        
class autorender(bpy.types.Operator):
    bl_idname = "render.autorender"
    bl_label = "Initialize"
    
    def execute(self, context):
        print ("Initializing")
        initializeBG()
        return {'FINISHED'}     
        
        
        
class autorender(bpy.types.Operator):
    bl_idname = "render.autorender"
    bl_label = "Initialize"
    
    def execute(self, context):
        print ("Initializing")
        initializeBG()
        return {'FINISHED'}

cl
    
  
    
bpy.utils.register_class(autorenderPanel)
bpy.utils.register_class(autorender)

'''