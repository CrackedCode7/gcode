from stl import mesh
import json
import tkinter as tk
from tkinter import filedialog

plot=True

root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()
root.destroy()

stlmesh = mesh.Mesh.from_file(file_path)
print("there are", len(stlmesh.points), "points in the file")

''' Plot the STL file if desired '''
if plot == True:
    from mpl_toolkits import mplot3d
    from matplotlib import pyplot
    # Create a new plot
    figure = pyplot.figure()
    axes = mplot3d.Axes3D(figure)
    # Add the vectors to the plot
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(stlmesh.vectors))
    # Auto scale to the mesh size
    scale = stlmesh.points.flatten(-1)
    axes.auto_scale_xyz(scale, scale, scale)
    # Show the plot to the screen
    pyplot.show()

''' Remove duplicate points and create dict for them '''
print('removing duplicate points and creating point dict')
points = {}
index=0
for ptset in stlmesh.vectors:
    for pt in ptset:
        pt = list(pt)
        for i in range(3):
            pt[i] = float(pt[i])
        for added_point in points:
            if pt == points[added_point]:
                #print("duplicate")
                break
        else:
            points[index] = pt
            index+=1
print('done')

''' Iterate over vectors to make a list of triangles '''
print('making a list of triangles')
triangles = []
for triangle in stlmesh.vectors:
    triangle = list(triangle)
    triangles.append(triangle)
    for i in range(3):
        triangles[-1][i] = list(triangles[-1][i])
print('done')

''' Create dictionary to map triangles and corresponding points '''
print('mapping triangles to points')
tridict = {}
i=0
for triangle in triangles:
    tridict[i] = []
    for point in triangle:
        for pt in points:
            if point == points[pt]:
                tridict[i].append(pt)
                break

    i+=1
print('done')

print('writing out map.json file')
outdict = {"points":points, "triangles":tridict}

with open("map.json","w") as write_file:
    json.dump(outdict, write_file, indent=4)

print('done writing out file, mapping complete')
