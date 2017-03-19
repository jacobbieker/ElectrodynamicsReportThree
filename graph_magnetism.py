import os, csv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

data_set_one = []
data_set_two = []
data_set_three = []

with open("just_data.txt", "r") as source:
    setup = 0
    for line in source:
        print(line)
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
def B_m(lg,lm,lk,hm):
    top = -1*lm*hm*u0
    bottom = lg*lk
    return top/bottom