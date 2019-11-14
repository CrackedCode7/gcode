# Make sure that the welder is placed on the base plate at the right center of the build.
# The code makes an arc from X0 to X4, then back to X0. Therefore be sure there is space in the Y direction.
# Suggested starting point is X2.5 and Y0

printingFeed=15
diameter=4
radius=diameter/2
z_height=4
z_step=.25
layers_for_dwell=10

print("G20 G91 F{}".format(printingFeed), file=open('cylinder_outline.tap','w'))
print("G1 Z{}".format(z_step), file=open('cylinder_outline.tap','a'))
print("m08", file=open('cylinder_outline.tap','a'))
print("G90 G02 X{}Y0 R{} F{}".format(diameter,radius,printingFeed), file=open('cylinder_outline.tap','a'))
print("G90 G02 X0Y0 R{} F{}".format(radius,printingFeed), file=open('cylinder_outline.tap','a'))
print("m09", file=open('cylinder_outline.tap','a'))
print("G91 G1 Z{}".format(z_step), file=open('cylinder_outline.tap','a'))

number_layers=round(z_height / z_step)

for i in range(number_layers):
    print("m08 G90", file=open('cylinder_outline.tap','a'))
    print("G02 X{}Y0 R{} F{}".format(diameter,radius,printingFeed), file=open('cylinder_outline.tap','a'))
    print("G02 X0Y0 R{} F{}".format(radius,printingFeed), file=open('cylinder_outline.tap','a'))
    print("m09", file=open('cylinder_outline.tap','a'))
    print("G91 G1 Z{}".format(z_step), file=open('cylinder_outline.tap','a'))
    if (i+1) % layers_for_dwell == 0:
        print("G04 P60", file=open('cylinder_outline.tap','a'))