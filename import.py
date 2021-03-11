import glob
import os
#initialize the world enviroment node 
    
    
def initialize(i):    
    
    C = bpy.context

    env_img = C.scene.world.node_tree.nodes['Environment Texture'].image

    world = C.scene.world
    world.use_nodes = True

    env_node = C.scene.world.node_tree.nodes.new("ShaderNodeTexEnvironment")
    
    node_tree = C.scene.world.node_tree 
    node_tree.links.new(env_node.outputs['Color'], node_tree.nodes['Background'].inputs['Color'])
    
    env_node.image = bpy.data.images.load(path_to + img_files[i])
    
    bpy.context.scene.render.film_transparent = False
    

####loading images into your .blend file

#fill this with whatever the path to your backgrounds is

def loadBg():
    path_to = 'D:/Programming/github/autorender/hdrs/'

    os.chdir(path_to)

    for file in glob.glob("*.hdr"):
        
        print(f'Loading file : {file}')
        bpy.data.images.load(path_to + file)