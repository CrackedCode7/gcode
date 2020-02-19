from stl import mesh
import json
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()
root.destroy()

stlmesh = mesh.Mesh.from_file(file_path)
print("there are", len(stlmesh.points), "elements in the file")

''' Find only triangles which intersect the slice height '''
print('searching for triangles intersecting the slice')
layer_height = 0
triangles = []
for triangle in stlmesh.vectors:
    for i in range(3):
        j = i+1
        if j == 3:
            j=0
        if triangle[i][2] <= layer_height <= triangle[j][2] or triangle[j][2] <= layer_height <= triangle[i][2]:
            triangles.append(triangle)
            break
print('done')

''' Remove duplicate points and create dict for them '''
print('removing duplicate points and creating point dict')
points = {}
index=0
for ptset in triangles:
    for pt in ptset:
        pt = list(pt)
        for i in range(3):
            pt[i] = float(pt[i])
        for added_point in points:
            if pt == points[added_point]:
                break
        else:
            points[index] = pt
            index+=1
print('done')

''' Iterate over vectors to make a list of triangles '''
print('making a list of triangles')
triangleList = []
for triangle in triangles:
    triangle = list(triangle)
    triangleList.append(triangle)
    for i in range(3):
        triangleList[-1][i] = list(triangleList[-1][i])
print('done')

''' Create dictionary to map triangles and corresponding points '''
print('mapping triangles to points (there are {})'.format(len(triangleList)))
tridict = {}
i=0
for triangle in triangleList:
    tridict[i] = []
    for point in triangle:
        for pt in points:
            if point == points[pt]:
                tridict[i].append(pt)
                break
    i+=1
print('done')

''' Write out map to JSON formatted file '''
print('writing out map.json file')
outdict = {"points":points, "triangles":tridict}
with open("map.json","w") as write_file:
    json.dump(outdict, write_file, indent=4)
print('done writing out file, mapping complete')
