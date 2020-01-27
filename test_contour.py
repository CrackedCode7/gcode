import csv
import math as mt

points = []
with open("testcase.csv",'r') as readFile:
    reader = csv.reader(readFile)
    for row in reader:
        points.append(row)

# remove duplicate line segments
restart=True
while restart==True:
    duplicateFound=False
    for i in range(len(points)):
        if points.index(points[i]) != i:
            #print('duplicate')
            points.pop(i)
            duplicateFound=True
            restart=True
            break
    if duplicateFound == False:
        restart=False

# Remove opposite direction line segments
restart=True
while restart==True:
    duplicateFound=False
    for point in points:
        index = points.index(point)
        new_list = points[:i] + points[i+1:]
        for newpt in new_list:
            if [point[0], point[1], point[2], point[3]] == [newpt[2], newpt[3], newpt[0], newpt[1]]:
                #print("remove")
                points.pop(index)
                duplicateFound=True
                restart=True
                break
        if duplicateFound == False:
            restart=False

polygon = []
'''
while len(points) > 0:
    polygon.append(points[0])
    points.pop(0)
    i=0
    while polygon[0][2] != polygon[len(polygon)][0] or polygon[0][3] != polygon[len(polygon)][1]:
        if points[i][0] == polygon[len(polygon)][2] and points[i][1] == polygon[len(polygon)][3]:
'''     


'''
# Create intersection point matrix

contour_points = []
distances = []
contour_points.append(points[0])
for i in range(1,len(points)):
    d1 = mt.sqrt((float(points[i][0]) - float(contour_points[0][2])) ** 2 + (float(points[i][1]) - float(contour_points[0][3])) ** 2)
    d2 = mt.sqrt((float(points[i][2]) - float(contour_points[0][2])) ** 2 + (float(points[i][3]) - float(contour_points[0][3])) ** 2)
    distances.append([d1,d2])
    if d2 < d1:
        #print("need to switch", d1, d2)
        points[i][0], points[i][1], points[i][2], points[i][3] = points[i][2], points[i][3], points[i][0], points[i][1]
        distances[i-1][0], distances[i-1][1] = distances[i-1][1], distances[i-1][0]

usableDistances = []
for i in range(len(distances)):
    if points[i][0] == contour_points[0][2] and points[i][1] == contour_points[0][3]:
        #print(i,distances[i],contour_points,points[i])
        usableDistances.append([i, distances[i]])

min_value = min(usableDistances)
min_index = usableDistances.index(min_value)
ptindex=usableDistances[min_index][0]
contour_points.append(points[ptindex])
print(contour_points)
points.pop(ptindex)

while len(points) != 0:
    distances = []
    for i in range(len(contour_points),len(points)):
        d1 = mt.sqrt((float(points[i][0]) - float(contour_points[len(contour_points)-1][2])) ** 2 + (float(points[i][1]) - float(contour_points[len(contour_points)-1][3])) ** 2)
        d2 = mt.sqrt((float(points[i][2]) - float(contour_points[len(contour_points)-1][2])) ** 2 + (float(points[i][3]) - float(contour_points[len(contour_points)-1][3])) ** 2)
        distances.append([d1,d2])
        if d2 < d1:
            #print("need to switch", d1, d2)
            points[i][0], points[i][1], points[i][2], points[i][3] = points[i][2], points[i][3], points[i][0], points[i][1]
            distances[i-len(contour_points)][0], distances[i-len(contour_points)][1] = distances[i-len(contour_points)][1], distances[i-len(contour_points)][0]

    usableDistances = []
    for i in range(len(distances)):
        if points[i][0] == contour_points[1][2] and points[i][1] == contour_points[1][3]:
            #print(i,distances[i],contour_points,points[i])
            usableDistances.append([i, distances[i]])

    min_value = min(usableDistances)
    min_index = usableDistances.index(min_value)
    ptindex=usableDistances[min_index][0]
    contour_points.append(points[ptindex])
    print(contour_points)
    points.pop(ptindex)
'''
