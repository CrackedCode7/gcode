from stl import mesh
import json
import matplotlib.pyplot as plt 
from matplotlib import collections as mc
import pylab as pl
import tkinter as tk
from tkinter import filedialog
import numpy as np

def get_STL_mesh():
    print("select STL file")
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    root.destroy()
    stlmesh = mesh.Mesh.from_file(file_path)
    print("there are", len(stlmesh.points), "triangles in the file")
    return stlmesh

def get_bounds(mesh):
    z = []
    for triangle in mesh.vectors:
        z.append(triangle[0][2])
        z.append(triangle[1][2])
        z.append(triangle[2][2])
    return min(z),max(z)

def get_intersect_segments(mesh, layer_height):
    print('finding segments intersecting the slice')
    segments = []
    for triangle in mesh.vectors:
        z = [triangle[0][2],triangle[1][2],triangle[2][2]]

        # Count number of direct intersections with slice
        count = sum(map(lambda x : x == layer_height, z))

        # Count number of points below slice
        count1 = sum(map(lambda x : x < layer_height, z))

        # Count number of points above slice
        count2 = sum(map(lambda x : x > layer_height, z))

        # If all points are above or below the slice, continue
        if count == 0 and count1 == 3 or count == 0 and count2 ==3:
            continue

        # Find Case 2 segments
        if count == 2:
            if z[0] == layer_height and z[1] == layer_height:
                segments.append([list(triangle[0]),list(triangle[1])])
            elif z[1] == layer_height and z[2] == layer_height:
                segments.append([list(triangle[1]),list(triangle[2])])
            elif z[0] == layer_height and z[2] == layer_height:
                segments.append([list(triangle[0]),list(triangle[2])])
            continue
        
        def find_points(point1,point2,layer_height):
                t = (layer_height - point1[2]) / (point2[2] - point1[2])
                x = point1[0] + t*(point2[0] - point1[0])
                y = point1[1] + t*(point2[1] - point1[1])
                return x,y
        
        # Find Case 3 segments
        if count == 0 and count1 == 1 and count2 == 2 or count == 0 and count1 == 2 and count2 == 1:
            if z[0] < layer_height and z[1] > layer_height and z[2] > layer_height:
                x1,y1 = find_points(triangle[0],triangle[1],layer_height)
                x2,y2 = find_points(triangle[0],triangle[2],layer_height)
                segments.append([[x1,y1,layer_height],[x2,y2,layer_height]])
                continue
            elif z[0] > layer_height and z[1] < layer_height and z[2] < layer_height:
                x1,y1 = find_points(triangle[0],triangle[1],layer_height)
                x2,y2 = find_points(triangle[0],triangle[2],layer_height)
                segments.append([[x1,y1,layer_height],[x2,y2,layer_height]])
                continue
            elif z[1] < layer_height and z[0] > layer_height and z[2] > layer_height:
                x1,y1 = find_points(triangle[1],triangle[0],layer_height)
                x2,y2 = find_points(triangle[1],triangle[2],layer_height)
                segments.append([[x1,y1,layer_height],[x2,y2,layer_height]])
                continue
            elif z[1] > layer_height and z[0] < layer_height and z[2] < layer_height:
                x1,y1 = find_points(triangle[1],triangle[0],layer_height)
                x2,y2 = find_points(triangle[1],triangle[2],layer_height)
                segments.append([[x1,y1,layer_height],[x2,y2,layer_height]])
                continue
            elif z[2] < layer_height and z[0] > layer_height and z[1] > layer_height:
                x1,y1 = find_points(triangle[2],triangle[0],layer_height)
                x2,y2 = find_points(triangle[2],triangle[1],layer_height)
                segments.append([[x1,y1,layer_height],[x2,y2,layer_height]])
                continue
            elif z[2] > layer_height and z[0] < layer_height and z[1] < layer_height:
                x1,y1 = find_points(triangle[2],triangle[0],layer_height)
                x2,y2 = find_points(triangle[2],triangle[1],layer_height)
                segments.append([[x1,y1,layer_height],[x2,y2,layer_height]])
                continue
        
        # Find Case 4 segments
        if count == 1 and count1 == 1 and count2 == 1:
            if z[0] == layer_height:
                x1,y1 = find_points(triangle[1],triangle[2],layer_height)
                segments.append([[x1,y1,layer_height],[triangle[0]]])
                continue
            elif z[1] == layer_height:
                x1,y1 = find_points(triangle[0],triangle[2],layer_height)
                segments.append([[x1,y1,layer_height],[triangle[1]]])
                continue
            elif z[2] == layer_height:
                x1,y1 = find_points(triangle[0],triangle[1],layer_height)
                segments.append([[x1,y1,layer_height],[triangle[2]]])
                continue

        # Find Case 5 segments
        if count == 3:
            segments.append([list(triangle[0]),list(triangle[1])])
            segments.append([list(triangle[1]),list(triangle[2])])
            segments.append([list(triangle[0]),list(triangle[2])])
            continue

    print('done finding intersecting segments')
    return segments

def get_unique_points(segments):
    points = {}
    index = 0
    for ptset in segments:
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
    print('done getting unique points')
    return points

def map_points_to_segments(segments,points):
    dictionary={}
    i = 0
    for segment in segments:
        dictionary[i] = []
        for point in segment:
            for pt in points:
                if point == points[pt]:
                    dictionary[i].append(pt)
                    break
        i+=1
    print('done mapping')
    return dictionary

def writemap(points,map,layer_height):
    outdict = {"points":points,"segments":map}
    with open(r"C:\Users\xsocc\OneDrive\Documents\coding\gcode-master\gcode-master\maps\\" + str(layer_height) + ".json","w") as write_file:
        json.dump(outdict,write_file,indent=4)
    print("done writing out map file")

def plot_layer(layer_height):
    with open(r"C:\Users\xsocc\OneDrive\Documents\coding\gcode-master\gcode-master\maps\\" + str(layer_height) + ".json","r") as read_file:
        data = json.load(read_file)
    points = data["points"]
    segments = data["segments"]

    remove=[]
    for segment in segments:
        for segment2 in segments:
            if segment == segment2:
                continue
            else:
                if set(segments[segment]) == set(segments[segment2]):
                    print(segments[segment],segments[segment2])
                    remove.append(segments[segment])
    remove = [list(item) for item in set(tuple(row) for row in remove)]
    remove1 = []
    print(remove)
    for item in remove:
        if sorted(item) not in remove1:
            remove1.append(sorted(item))
            print('something')
        else:
            print('somehting else')
    print(remove1)
    delete = [key for key in segments if segments[key] in remove1]
    for key in delete: del segments[key]

    lines = []
    for segment in segments:
        lines.append([(points[str(segments[segment][0])][0],points[str(segments[segment][0])][1]),(points[str(segments[segment][1])][0],points[str(segments[segment][1])][1])])

    lc = mc.LineCollection(lines)
    fig, ax = pl.subplots()
    ax.add_collection(lc)
    ax.autoscale()
    ax.margins(0.1)
    plt.show()

mesh = get_STL_mesh()
bounds = get_bounds(mesh)

layers = list([bounds[0]])
for layer in layers:
    segments = get_intersect_segments(mesh,layer)
    points = get_unique_points(segments)
    map1 = map_points_to_segments(segments,points)
    writemap(points,map1,layer)
    plot_layer(layer)
