from stl import mesh

# Load the STL files and add the vectors to the plot
stlmesh = mesh.Mesh.from_file("cube_hollow.STL")

# Converts STL units to inches
for i in range(len(stlmesh.vectors)):
    for j in range(len(stlmesh.vectors[i])):
        stlmesh.vectors[i][j] = stlmesh.vectors[i][j] / 25.4

points = []
for vector in stlmesh.vectors:
    for point in vector:
        points.append(point)

restart=True
while restart==True:
    duplicateFound=False
    for num in range(len(points)):
        print(point)
        new_list = points[:num] + points[num+1:]
        for newpt in new_list:
            if len(list(set(point) - set(newpt))) == 0:
                print("remove")
                points.pop(num)
                duplicateFound=True
                restart=True
                break
        if duplicateFound == False:
            restart=False
