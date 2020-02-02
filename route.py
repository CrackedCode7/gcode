from stl import mesh

# Load the STL files and add the vectors to the plot
stlmesh = mesh.Mesh.from_file("ArtecSpiderNerfGunmm.stl")

print("there are", len(stlmesh.points), "points in the file")

points = {}
index=0
for ptset in stlmesh.vectors:
    for pt in ptset:
        pt = list(pt)
        for added_point in points:
            if pt == points[added_point]:
                print("duplicate")
                break
        else:
            points[index] = pt
            print("added point",index)
            index+=1
        break

