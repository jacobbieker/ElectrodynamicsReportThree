import os, csv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from operator import itemgetter

data_set_one = []
data_set_two = []
data_set_three = []

with open("just_data.txt", "r") as source:
    setup = 0
    for line in source:
        if line != "NEW\n":
            parts = line.split(",")
            x = float(parts[0])
            y = float(parts[1])
            gauss = float(parts[2])
            if setup == 0:
                data_set_one.append((x,y,gauss))
            elif setup == 1:
                data_set_two.append((x,y,gauss))
            elif setup == 2:
                data_set_three.append((x,y,gauss))
            else:
                print("Goes beyond three setups")
        else:
            setup += 1

# Now display a heat map of the whole things
# Try to find how large the magnet would be in the photo, or the bars
# Magnet is apparently 25mm on a side, so can make a block out of that
# But size doesnt matter apparently, see how it goes, don't have a value for the size of the iron yokes

# Part A results
x, y, gauss = zip(*data_set_one)
heatmap, xedges, yedges = np.histogram2d(x, y, weights=gauss, bins=30)
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

plt.clf()
plt.imshow(heatmap.T, extent=extent, origin='lower')
plt.title("Part A: 4mm thick gap")
plt.xlabel("X position (mm)")
plt.ylabel("Y position (mm)")
currentAxis = plt.gca()
currentAxis.add_patch(Rectangle((0, 0), 26, 26, facecolor="none"))
plt.show()

# Part B results
x, y, gauss = zip(*data_set_two)
heatmap, xedges, yedges = np.histogram2d(x, y, weights=gauss, bins=30)
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

plt.clf()
plt.imshow(heatmap.T, extent=extent, origin='lower')
plt.title("Part B: 4mm thick gap")
plt.xlabel("X position (mm)")
plt.ylabel("Y position (mm)")
currentAxis = plt.gca()
currentAxis.add_patch(Rectangle((0, 0), 26, 26, facecolor="none"))
plt.show()


# Part C results
x, y, gauss = zip(*data_set_three)
heatmap, xedges, yedges = np.histogram2d(x, y, weights=gauss, bins=30)
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

plt.clf()
plt.imshow(heatmap.T, extent=extent, origin='lower')
plt.title("Part C: 2mm thick gap")
plt.xlabel("X position (mm)")
plt.ylabel("Y position (mm)")
currentAxis = plt.gca()
currentAxis.add_patch(Rectangle((0, 0), 26, 26, facecolor="none"))
plt.show()

# Part C Differences results
x, y, gauss = zip(*data_set_two)
x1, y1, gauss1 = zip(*data_set_three)

"""
# Get differences in field strength for these values
x = abs(x) - abs(x1)
y = abs(y) - abs(y1)
gauss = abs(gauss) - abs(gauss1)

heatmap, xedges, yedges = np.histogram2d(x, y, weights=gauss, bins=100)
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

plt.clf()
plt.imshow(heatmap.T, extent=extent, origin='lower')
plt.title("Part B")
plt.show()
"""

# Getting B(m)
u0 = 4.*np.pi*(10**(-7))
l_m = 25.*2
l_g = 4.
l_k = 1.*4

def B_m(lg,lm,lk,hm):
    # Gets B(m) from measured values?
    top = -1*lm*hm*u0
    bottom = lg*lk
    return top/bottom

# Integration though doing flux * area from the measurements
# Part A first, each value corresponds to a 5x5mm section. So no interpolation at the moment, might try later
total_a = 0
for value in data_set_one:
    total_a += value[2]*25 #mm^2
print(total_a)
# B is 10x10mm, so 100mm^2
total_b = 0
for value in data_set_two:
    total_b += value[2]*100 #mm^2
print(total_b)

from scipy import interpolate

sorted_data_one = sorted(data_set_one,key=itemgetter(0,1))
sorted_data_two = sorted(data_set_two,key=itemgetter(0,1))
sorted_data_three = sorted(data_set_three,key=itemgetter(0,1))

x_1, y_1, gauss1 = zip(*sorted_data_one)
x_2, y_2, gauss2 = zip(*sorted_data_two)
x3, y3, gauss3 = zip(*sorted_data_three)

gauss1 = np.asarray(gauss1)
gauss2 = np.asarray(gauss2)
gauss3 = np.asarray(gauss3)

x1 = []
y1 = []
for index, element in enumerate(x_1):
    print(element)
    x1.append(element + abs(min(x_1)))

for index, element in enumerate(y_1):
    y1.append(element + abs(min(y_1)))

# Redoing it my way

one_array = np.empty([int(max(x1)), int(max(y1))])
one_array[:] = np.NAN
print(one_array)
print(y1)
print(x1)
for element in sorted_data_one:
    one_array[int(element[0]), int(element[1])] = element[2]
    print(one_array[int(element[0])])
x_list = []
y_list = []
for index in range(0,int(max(x1))):
    x_list.append(index)
for index in range(0,int(max(y1))):
    y_list.append(index)

x1_spline = interpolate.RectBivariateSpline(x_list, y_list, one_array)
print(one_array)

x2 = []
y2 = []
for index, element in enumerate(x_2):
    print(element)
    x2.append(element + abs(min(x_2)))

for index, element in enumerate(y_2):
    y2.append(element + abs(min(y_2)))

# Redoing it my way

two_array = np.empty([int(max(x2)), int(max(y2))])
two_array[:] = np.NAN
print(two_array)
print(y2)
print(x2)
for element in sorted_data_two:
    two_array[int(element[0]), int(element[1])] = element[2]
x_list2 = []
y_list2 = []
for index in range(0,int(max(x2))):
    x_list2.append(index)
for index in range(0,int(max(y2))):
    y_list2.append(index)

x2_spline = interpolate.RectBivariateSpline(x_list2, y_list2, two_array)


print(x1_spline.integral(0.,max(x1),0.,max(y1)))

print(x2_spline.integral(0.,max(x2),0.,max(y2)))

print(x1_spline(x_list, y_list))

print(x1_spline.get_coeffs())

#mask invalid values
array = np.ma.masked_invalid(one_array)
xx, yy = np.meshgrid(x_list, y_list)
#get only the valid values
x1 = xx[~array.mask]
y1 = yy[~array.mask]
newarr = array[~array.mask]

GD1 = interpolate.griddata((x1, y1), newarr.ravel(),
                          (xx, yy),
                             method='cubic')
print(GD1)
plt.imshow(GD1,interpolation='nearest')
plt.show()

#mask invalid values
array = np.ma.masked_invalid(two_array)
xx, yy = np.meshgrid(y_list2, x_list2)
#get only the valid values
x1 = xx[~array.mask]
y1 = yy[~array.mask]
newarr = array[~array.mask]

GD2 = interpolate.griddata((x1, y1), newarr.ravel(),
                          (xx, yy),
                             method='cubic')
print(GD2)
plt.imshow(GD2,interpolation='nearest')
plt.show()

total_b = np.nansum(GD2)
total_a = np.nansum(GD1)

print(total_a)
print(total_b)
