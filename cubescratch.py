import bpy
from math import *
import colorsys

cubeLen = 35
space = 2
x = 1
y = 1

#Finds the normalized distance of a cube from the center of the grid
def centerDist():
    deltaX = abs(cubeLen - x)
    deltaY = abs(cubeLen - y)
    dist = sqrt(deltaX * deltaX + deltaY * deltaY)
    maxdist = sqrt(2*(cubeLen/2 * cubeLen/2))
    normdist = dist/maxdist
    return normdist

#Creates a material and applies a diffuse color 
def color():
    current = bpy.context.object
    r,g,b = colorsys.hsv_to_rgb(centerDist(), 0.875, 1.0)
    mat = bpy.data.materials.new(name='Surface')
    mat.diffuse_color = (r, g, b, 1.0)
    current.data.materials.append(mat)

#Changes color, creates and sets Keying Set, then creates keyframes.   
def animateColor():
    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = 165
    frange = 165
    fcount = 12
    invfcount = 1 / fcount
    frameIncrement = frange * invfcount
    current = bpy.context.object
    mat = bpy.data.materials.new(name='Surface')
    r,g,b = colorsys.hsv_to_rgb(centerDist(), 0.875, 1.0)
    mat.diffuse_color = (r, g, b, 1.0)
    current.data.materials.append(mat)
    currframe = 0
    scene = bpy.context.scene
    ks = scene.keying_sets.new(idname="Keyingset", name="Keyingset")
    ksp = ks.paths.add(mat, 'diffuse_color', index=-1)
    hueStep = 0
    #Number of times to increment red upwards
 
    for f in range (0, fcount):
        fprc = f * (1/(fcount-1))
        angle = 2*pi * fprc
        offset = -2*pi * centerDist() + pi
        print(fprc)
        print(angle)
        print(offset)
        bpy.context.scene.frame_set(currframe)
        current.scale[2] = 0.125 + abs(sin(offset + angle)) * 3.4
        r,g,b = colorsys.hsv_to_rgb(centerDist() + hueStep, 0.875, 1)
        mat.diffuse_color = (r, g, b, 1.0)
        bpy.ops.anim.keyframe_insert(type='__ACTIVE__')
        current.keyframe_insert(data_path='scale', index=2)
        hueStep += 0.1
        currframe += frameIncrement

#The main loop that creates the grid and applies the colors/animation
for i in range(0, cubeLen):
    bpy.ops.mesh.primitive_cube_add(location=(x,y,1))
    animateColor()
    y = y + space
    for j in range (1, cubeLen):
        bpy.ops.mesh.primitive_cube_add(location=(x,y,1))
        animateColor()
        y = y + space
    x = x + space
    y = 1