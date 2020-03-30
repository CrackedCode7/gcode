from stl import mesh
from mpl_toolkits.mplot3d import Axes3D
import json
import matplotlib.pyplot as plt 
import tkinter as tk
from tkinter import filedialog
import numpy as np

# Reads in STL mesh from file
def get_STL_mesh():
    print("select STL file")
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    root.destroy()
    stlmesh = mesh.Mesh.from_file(file_path)
    print("there are", len(stlmesh.points), "triangles in the file")
    return stlmesh

# Finds bounds (Z) of STL mesh 
def get_bounds(mesh):
    z = []
    for triangle in mesh.vectors:
        z.append(triangle[0][2])
        z.append(triangle[1][2])
        z.append(triangle[2][2])
    return min(z),max(z)

# Finds intersect segments of STL triangles with the layer height (slice)
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
        
        # Define a function to find intersection points based on 3D lines
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

# Check all points against each other and find unique points
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

# Map unique points to intersection segments
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

# Plot the intersection segments (one plot at end with all layers) and write out JSON file for each layer
def plot_layer(points,dictionary,layer_number):
    outdict = {"points":points,"segments":dictionary}
    points = outdict["points"]
    segments = outdict["segments"]
    print(segments)
    
    '''
    # Perform head to tail check and form polygons
    polygons = []
    while len(segments) > 0:
        polygons.append([])
        for segment in segments:
            if len(polygons[-1]) == 0:
                polygons[-1].append(segments(segment))
                del segments[segment]
            while polygons[-1][0] != polygons[-1][-1]:
                for segment in segments:
                    if polygons[-1][0] == segments[segment][0] or polygons[-1][1] == segments[segment][1]:
                        print('found next one, need to switch orientation')
                        polygons[-1].append(segments[segment])
                        del segments[segment]
                    elif polygons[-1][0] == segments[segment][1] or polygons[-1][1] == segments[segment][0]:
                        print('found next one, correct orientation')
                        polygons[-1].append(segments[segment])
                        del segments[segment]
    '''

    for segment in segments:
        x = [points[segments[segment][0]][0],points[segments[segment][1]][0]]
        y = [points[segments[segment][0]][1],points[segments[segment][1]][1]]
        z = [points[segments[segment][0]][2],points[segments[segment][1]][2]]
        ax.plot(x, y, z, color='blue')

    with open(str(layer_number) + '.json','w') as writeFile:
        json.dump({"points":points,"segments":segments},writeFile,indent=4)

# Call functions to get required information
mesh = get_STL_mesh()
bounds = get_bounds(mesh)

# Create a plot, set the axes to 3D
fig = plt.figure()
ax = fig.gca(projection='3d')

# Iterate over some number of layers, calling all required functions to plot and write out files
layers = list(np.linspace(bounds[0] + 1e-6,bounds[1] - 1e-6,10))
layer_number = 1
for layer in layers:
    segments = get_intersect_segments(mesh,layer)
    points = get_unique_points(segments)
    map1 = map_points_to_segments(segments,points)
    plot_layer(points,map1,layer_number)
    layer_number+=1

# Scale plot axes, save figure of all layers
ax.autoscale()
ax.margins(0.1)
plt.savefig('all.png')
plt.close()
