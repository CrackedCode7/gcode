from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
import numpy as np

layerHeight = .25 #estimated height of each layer

# Load the STL files and add the vectors to the plot
stlmesh = mesh.Mesh.from_file("cube_hollow.STL")

# Converts STL units to inches
for i in range(len(stlmesh.vectors)):
    for j in range(len(stlmesh.vectors[i])):
        stlmesh.vectors[i][j] = stlmesh.vectors[i][j] / 25.4

# Show the STL mesh
figure=pyplot.figure()
ax = mplot3d.Axes3D(figure)

points = []
for vector in stlmesh.vectors:
    for point in vector:
        points.append(point)

points = np.asarray(points)
x = points[:,0]
y = points[:,1]
z = points[:,2]

# Iterate over all points, finding only ones at a zero layer height
currentLayerTriangles = []
for triangle in stlmesh.vectors:
    if triangle[0][2] == 0 and triangle[1][2] == 0 and triangle[2][2] == 0:
        currentLayerTriangles.append(triangle)

ax.plot(x,y,z)
#ax.scatter(x,y,z)
#pyplot.show()

# Iterate over the build height to create slices
height = 0
while height < max(z):
    height+=layerHeight
    #print(height)
