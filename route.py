from stl import mesh

# Load the STL files and add the vectors to the plot
stlmesh = mesh.Mesh.from_file("ArtecSpiderNerfGunmm.stl")
print(stlmesh.points)
