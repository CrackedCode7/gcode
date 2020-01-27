import re
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

filename=open("cube.STL")

points_x = []
points_y = []
points_z = []
for line in filename:
    if "vertex" in line:
        print(line)
        xnumber = re.findall(r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?', line )[0][0]
        xexponent = re.findall(r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?', line )[0][2]
        xreal_exponent = int(re.findall(r'\d+', xexponent)[0])
        points_x.append(float(xnumber)*10**xreal_exponent)

        ynumber = re.findall(r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?', line )[1][0]
        yexponent = re.findall(r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?', line )[1][2]
        yreal_exponent = int(re.findall(r'\d+', yexponent)[0])
        points_y.append(float(ynumber)*10**yreal_exponent)

        znumber = re.findall(r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?', line )[2][0]
        zexponent = re.findall(r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?', line )[2][2]
        zreal_exponent = int(re.findall(r'\d+', zexponent)[0])
        points_z.append(float(znumber)*10**zreal_exponent)

ax = plt.axes(projection='3d')
ax.plot3D(points_x, points_y, points_z,'--')
plt.show()
