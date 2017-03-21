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
lm = 25.*2
lg = 4.
lk = 1.*4

def B_m(hm):
    # Gets B(m) from measured values?
    top = -1*lm*hm*u0
    bottom = lg+lk
    return bottom/top

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
    x1.append(element + abs(min(x_1)))

for index, element in enumerate(y_1):
    y1.append(element + abs(min(y_1)))

#sorted_data_one = zip(x_1,y_1,gauss1)
# Redoing it my way
x_list = []
y_list = []
for index in range(0,int(max(x1))+1):
    x_list.append(index)
for index in range(0,int(max(y1))+1):
    y_list.append(index)

one_array = np.empty([int(max(x1))+1, int(max(y1))+1])
one_array[:] = np.NAN
#print(sorted_data_one)
for index, element in enumerate(sorted_data_one):
    one_coor = element[0]
    two_coor = element[1]
    one_coor += abs(min(x_1))
    two_coor += abs(min(y_1))
    #print(one_array.shape[1])
    #print(len(sorted_data_one))
    one_array[int(one_coor), int(two_coor)] = element[2]

x1_spline = interpolate.RectBivariateSpline(x_list, y_list, one_array)
print(one_array)

x2 = []
y2 = []
for index, element in enumerate(x_2):
    #print(element)
    x2.append(element + abs(min(x_2)))

for index, element in enumerate(y_2):
    y2.append(element + abs(min(y_2)))

# Redoing it my way

x_list2 = []
y_list2 = []
for index in range(0,int(max(x2))+1):
    x_list2.append(index)
for index in range(0,int(max(y2))+1):
    y_list2.append(index)

two_array = np.empty([int(max(x2))+1, int(max(y2))+1])
two_array[:] = np.NAN
#print(two_array)
#print(y2)
#print(x2)
for index, element in enumerate(sorted_data_two):
    one_coor = element[0]
    two_coor = element[1]
    one_coor += abs(min(x_2))
    two_coor += abs(min(y_2))
    #print(one_array.shape[1])
    #print(len(sorted_data_one))
    two_array[int(one_coor), int(two_coor)] = element[2]

x2_spline = interpolate.RectBivariateSpline(x_list2, y_list2, two_array)


#print(x1_spline.integral(0.,max(x1),0.,max(y1)))

#print(x2_spline.integral(0.,max(x2),0.,max(y2)))

#print(x1_spline(x_list, y_list))

#print(x1_spline.get_coeffs())

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
#print(GD1)
plt.imshow(GD1,interpolation='nearest')
plt.title("Part A: 4mm thick gap")
plt.xlabel("X position (mm)")
plt.ylabel("Y position (mm)")
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
#print(GD2)
plt.imshow(GD2,interpolation='nearest')
plt.title("Part B: 4mm thick gap")
plt.xlabel("X position (mm)")
plt.ylabel("Y position (mm)")
plt.show()

total_b = np.nansum(GD2)
total_a = np.nansum(GD1)

print(total_a)
print(total_b)

# Part 2: Get the flux inside the gab, so only within the area of the gab roughly [0,30] on both sides

x21, y21, gauss21 = zip(*sorted_data_two)
x3, y3, gauss3 = zip(*sorted_data_three)

# Get only data inside the gab
partb_one = []
for index, element in enumerate(x21):
    if 0.0 <= element <= 30.0 and 0.0 <= y21[index] <= 30.0:
        partb_one.append(gauss21[index])

partb_two = []
for index, element in enumerate(x3):
    if 0.0 <= element <= 30.0 and 0.0 <= y3[index] <= 30.0:
        partb_two.append(gauss3[index])

total_partb_one = np.sum(partb_one)
total_partb_two = np.sum(partb_two)

print(total_partb_one)
print(total_partb_two)

# H(m), using B_m reveresed for this
print(B_m(total_partb_one))
print(B_m(total_partb_two))

hm_partb_one = B_m(total_partb_one)
hm_partb_two = B_m(total_partb_two)

data_part_two_bm = [total_partb_two, total_partb_one]
data_part_two_hm = [hm_partb_two, hm_partb_one]

fit = np.polyfit(data_part_two_bm, data_part_two_hm, 1)
print(fit)
fit_x = np.arange(0, 200000, 1000)
plt.plot(data_part_two_bm, data_part_two_hm)
plt.plot(fit_x, fit_x*fit[0] + fit[1])
plt.xlabel("B(m) Telsa")
plt.ylabel("H(m) Tesla")
plt.title("B(m) vs H(m) for Different Gaps")
plt.show()

