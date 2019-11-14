# This script is meant to start at a height of zero and in the top right corner of the build plate
# Be sure to set the welder in the proper initial position ON the build plate to ensure each layer is consistent.

printingFeed=15
x_distance=4
y_distance=4
z_height=4
z_step=.25
layers_for_dwell=10

print("G91 G20", file=open('cube_outline.tap','w'))
print("G1 Z{}".format(z_step), file=open('cube_outline.tap','a'))
print("m08", file=open('cube_outline.tap','a'))
print("G1 X-{}".format(x_distance)+" F{}".format(printingFeed), file=open('cube_outline.tap','a'))
print("G1 Y-{}".format(y_distance), file=open('cube_outline.tap','a'))
print("G1 X{}".format(x_distance), file=open('cube_outline.tap','a'))
print("G1 Y{}".format(y_distance), file=open('cube_outline.tap','a'))
print("m09", file=open('cube_outline.tap','a'))
print("G1 Z{}".format(z_step), file=open('cube_outline.tap','a'))

number_layers=round(z_height / z_step)

for i in range(number_layers):
    print("m08", file=open('cube_outline.tap','a'))
    print("G1 X-{}".format(x_distance), file=open('cube_outline.tap','a'))
    print("G1 Y-{}".format(y_distance), file=open('cube_outline.tap','a'))
    print("G1 X{}".format(x_distance), file=open('cube_outline.tap','a'))
    print("G1 Y{}".format(y_distance), file=open('cube_outline.tap','a'))
    print("m09", file=open('cube_outline.tap','a'))
    print("G1 Z{}".format(z_step), file=open('cube_outline.tap','a'))
    if (i+1) % layers_for_dwell == 0:
        print("G04 P60", file=open('cube_outline.tap','a'))

''' CHANGE LOG FROM PREVIOUS version
The only change in this version of the code from the previous one is a line added right after the code starts to
lift the welder off of the base plate and start welding at the height specified as z_step. This addition allows us 
to ensure the height between layers is the same for each layer, even the first one.'''