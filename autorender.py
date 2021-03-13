import math
import bpy
from bpy import context
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
        
    

def autoRenderCycle(cycles):
    
    scene = context.scene
    
    initializeBG()
    
    chair = bpy.data.objects['Chair']
    
    chair.location = Vector((0,0,0.5))

    cam = bpy.data.objects['Camera']

    bpy.ops.object.select_all(action='DESELECT')
    
    cam.select_set(True)
    scene.camera = context.object
    
    for c in range(cycles):
        print(c)
        x = random.uniform(-3,3)
        y = random.uniform(-3,3)
        if (x >= -1.5 and x <= 1.5) and (y >= -1.5 and y <= 1.5):
            z = random.uniform(3,5)
        else:
            z = random.uniform(0,4)
        cam.location = Vector((x, y, z))
        print('Moving Camera...')
        
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.scene.render.image_settings.color_mode ='RGBA'
        bpy.context.scene.render.image_settings.file_format='PNG' 
        bpy.context.scene.render.image_settings.compression = 90
        
        img_random = random.randint(0, len(bpy.data.images))
        print(img_random)
        if bpy.data.images[img_random].name == 'Render Result':
            bpy.data.images.remove(bpy.data.images[img_random])
            img_random = random.randint(0, len(bpy.data.images))
            
        env_node.image = bpy.data.images[img_random]
        print(env_node.image)

        bpy.context.scene.render.filepath = os.path.join(path_to_output, f'{img_name}-{str(c)}.png')
        bpy.ops.render.render(write_still=True)



class autorenderPanel(bpy.types.Panel):
    bl_label = "Auto Render"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"
    bl_category = "Autorender"
    
    
    def draw(self, context):
    
        layout = self.layout
        layout.label(text='Autorendering script')
        layout.operator("render.autorender", text="Begin Autorendering")
        
       
        
class autorender(bpy.types.Operator):
    bl_idname = "render.autorender"
    bl_label = "Autorender"
    
    def execute(self, context):
        print ("Rendering..")
        autoRenderCycle(10)
        return {'FINISHED'}
      
    

def register():
    bpy.utils.register_class(autorenderPanel)
    bpy.utils.register_class(autorender)


def unregister():
    bpy.utils.unregister_class(autorenderPanel)
    bpy.utils.unregister_class(autorender)
    
if __name__ == "__main__":
    register()