import re
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

filename=open("cube.STL")

points = []
for line in filename:
    if "vertex" in line:
        xnumber = re.findall(r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?', line )[0][0]
        xexponent = re.findall(r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?', line )[0][2]
        xreal_exponent = int(re.findall(r'\d+', xexponent)[0])
        point_x = float(xnumber)*10**xreal_exponent

        ynumber = re.findall(r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?', line )[1][0]
        yexponent = re.findall(r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?', line )[1][2]
        yreal_exponent = int(re.findall(r'\d+', yexponent)[0])
        point_y = float(ynumber)*10**yreal_exponent

        znumber = re.findall(r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?', line )[1][0]
        zexponent = re.findall(r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?', line )[1][2]
        zreal_exponent = int(re.findall(r'\d+', zexponent)[0])
        point_z = float(znumber)*10**zreal_exponent
        lst=[point_x, point_y, point_z]
        points.append(lst)

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D(points[0][0], points[0][1], points[0][2], 'gray')
plt.show
