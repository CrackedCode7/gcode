import json
import matplotlib.pyplot as plt
from matplotlib import collections as mc
import pylab as pl

with open("map.json", "r") as read_file:
    data = json.load(read_file)

points = data["points"]
triangles = data["triangles"]

z = []
for point in points:
    z.append(points[point][2])
zmin = min(z)
print(zmin,'is the minimum z height')

# Find points that are on the base layer
basepts = []
for point in points:
    if points[point][2] == zmin:
        basepts.append(int(point))

# Check whether a triangle is on the base layer
checkTriangles = []
for triangle in triangles:
    if all(item in basepts for item in triangles[triangle]):
        checkTriangles.append(triangle)

# Add vectors for each triangle
vectors = {}
for triangle in checkTriangles:
    vectors[triangle] = []
    for pt1 in triangles[triangle]:
        for pt2 in triangles[triangle]:
            if pt1 == pt2:
                continue
            elif pt1 > pt2:
                continue
            else:
                vectors[triangle].append([pt1,pt2])

# Remove duplicate vectors
remove = []
for vector in vectors: # for each set of vectors for a triangle
    for vector2 in vectors: # for each other set of vectors for another triangle
        if vector == vector2: # skip if the triangles are the same
            continue
        else: # loop over all vectors in the triangles
            for i in range(len(vectors[vector])):
                for j in range(len(vectors[vector2])):
                    if set(vectors[vector][i]) == set(vectors[vector2][j]): # if the vectors are the same, record them
                        remove.append(vectors[vector][i])

remove = [list(item) for item in set(tuple(row) for row in remove)]

for vector in vectors:
    i=0
    while i < len(vectors[vector]):
        if vectors[vector][i] in remove:
            vectors[vector].pop(i)
            i=0
        else:
            i+=1

lines=[]
for vector in vectors:
    for pts in vectors[vector]:
        lines.append([(points[str(pts[0])][0],points[str(pts[0])][1]),(points[str(pts[1])][0],points[str(pts[1])][1])])

lc = mc.LineCollection(lines)
fig, ax = pl.subplots()
ax.add_collection(lc)
ax.autoscale()
ax.margins(0.1)
plt.show()
