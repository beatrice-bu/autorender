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


def autorender(cycles):    
    
    try:
        '''
        Some initial setup
        '''
        # Shortcut for the very important 'bpy.context' class
        C = bpy.context 
        #Shortcut for world, this is how we get information on the items in the scene
        world = C.scene.world
        #Activating the use of nodes, which are what I will control the environment with
        world.use_nodes = True
        #another neccesary shortcut for controlling the objects within the scecne
        scene = context.scene

        
        global env_node
        
        #This is the environment node I will use.
        env_node = C.scene.world.node_tree.nodes.new("ShaderNodeTexEnvironment")
        
        #shortcut for the node_tree class
        node_tree = C.scene.world.node_tree
        #another step in activating the new environment node
        node_tree.links.new(env_node.outputs['Color'], node_tree.nodes['Background'].inputs['Color'])
        #this makes sure the environment is visible
        bpy.context.scene.render.film_transparent = False
        
        #searching through to find all of the files in the environments folder
        for file in glob.glob(path_to_hdrs + '*.hdr'):
            #load every file you find
            bpy.data.images.load(file)
    
    finally:
        '''
        Now that the initialization phase it out of the way, we can start rendering
        I'm not entirely sure if try-finally was the best way to do this. I figured
        it would control the flow of these two seperate actions. Alternatively I could 
        make them seperate functions, but experience has proven this is the most stable
        way to control the procedure
        '''
        print('Beginning Auto-Render')

        #making a pointer for the chair(target), camera and seperate lighting in my scene
        cam = bpy.data.objects['Camera']
        chair = bpy.data.objects['Chair']
        light = bpy.data.objects['Light']
        #ensuring the object is centered at world origin.
        chair.location = Vector((0,0,0.5))
        
        #deselect everything to remove context
        bpy.ops.object.select_all(action='DESELECT')

        #selects only the camera present in the scene so the frame of the image is correct
        cam.select_set(True)
        scene.camera = context.object

        '''
        Cycling
        Every loop moves the camera and lighting, changes the environment
        and then finally renders the image and saves it in the output folder
        '''
        for c in range(cycles):
            
            print(f' Cycle {c} out of {cycles}')


            print('Moving Camera...')
            #picking random locations relatively near the target. Camera is locked on to the target,
            #so wherever it goes, it will point towards it, giving us different distances and angles.
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
    autorender()

