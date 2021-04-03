import math
import bpy
from bpy import context
import mathutils
import os
import glob
import random
from mathutils import Vector

path_to_hdrs = '\\home\\beatrice_au_bu\\autorender\\hdrs\\'
path_to_output = '/home/beatrice_au_bu/output'
img_name = 'chair'


def initialize():    
    
    C = bpy.context
    world = C.scene.world
    world.use_nodes = True

    global env_node
    env_node = C.scene.world.node_tree.nodes.new("ShaderNodeTexEnvironment")
    
    node_tree = C.scene.world.node_tree
    node_tree.links.new(env_node.outputs['Color'], node_tree.nodes['Background'].inputs['Color'])
    
    bpy.context.scene.render.film_transparent = False
    
    for file in glob.glob(path_to_hdrs + '*.hdr'):
        
        bpy.data.images.load(file)
    autoRenderCycle(1)

def autoRenderCycle(cycles):
    
    print('Beginning Auto-Render')
    
    chair = bpy.data.objects['Chair']
    
    chair.location = Vector((0,0,0.5))
    
    scene = context.scene
    cam = bpy.data.objects['Camera']

    light = bpy.data.objects['Light']

    bpy.ops.object.select_all(action='DESELECT')

    cam.select_set(True)
    scene.camera = context.object

    for c in range(cycles):
        
        print(f' Cycle {c} out of {cycles}')


        print('Moving Camera...')
        x = random.uniform(-2.5,2.5)
        y = random.uniform(-2.5,2.5)
        if (x >= -1.5 and x <= 1.5) and (y >= -1.5 and y <= 1.5):
            z = random.uniform(3,4)
        else:
            z = random.uniform(0,4)

        cam.location = Vector((x, y, z))

        print('Moving Light...')
        x = random.uniform(-1.5,1.5)
        y = random.uniform(-1.5,1.5)
        light.location = Vector((x, y, z))

        print('Setting up render...')
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.scene.render.image_settings.color_mode ='RGBA'
        bpy.context.scene.render.image_settings.file_format='PNG' 
        bpy.context.scene.render.image_settings.compression = 90
        
        
        print('Choosing enviroment...')
        img_random = random.randint(0, len(bpy.data.images)- 1)
        
        print(img_random)
        
        if bpy.data.images[img_random].name == 'Render Result':
            bpy.data.images.remove(bpy.data.images[img_random]) 
            img_random = random.randint(0, len(bpy.data.images))
            
        env_node.image = bpy.data.images[img_random]
        print(env_node.image)
        print('\n')

        bpy.context.scene.render.filepath = os.path.join(path_to_output, f'{img_name}-{str(c)}.png')
        bpy.ops.render.render(write_still=True)
        
        bpy.data.images.remove(bpy.data.images['Render Result'])
        
if __name__ == "__main__":
   initialize()

