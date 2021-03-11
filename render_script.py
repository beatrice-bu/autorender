from random import uniform
from mathutils import Vector
import bpy





bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0, 0, 0), rotation=(1.24267, -7.30479e-07, -0.418879), scale=(1, 1, 1))
bpy.ops.wm.collada_import(filepath="D:\\Programming\\github\\image-gen\\models\\chair.dae")
bpy.ops.object.select_all(action='DESELECT')


chair = bpy.data.objects['Chair']
chair.location = Vector((0,0,0.5))


cam = bpy.data.objects['Camera']

bpy.ops.object.select_all(action='DESELECT')


cam.select_set(True)
cam = bpy.context.object

bpy.ops.object.constraint_add(type='TRACK_TO')
bpy.context.object.constraints["Track To"].target = bpy.data.objects["Chair"]
bpy.context.object.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'



cam = bpy.data.objects['Camera']
def randX():
    x = uniform(-5,5)
    y = uniform(-5,5)
    if (x >= -1.5 and x <= 1.5) and (y >= -1.5 and y <= 1.5):
        z = uniform(3,5)
    else:
        z = uniform(0,5)
    cam.location = Vector((x, y, z))
    


randX()




