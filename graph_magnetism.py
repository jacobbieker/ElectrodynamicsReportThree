import os, csv
import matplotlib.pyplot as plt
import numpy as np

data_set_one = []
data_set_two = []
data_set_three = []

with open("just_data.txt", "r") as source:
    setup = 0
    for line in source:
        if line is not "" or line is not None:
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

# Part A results
x, y, gauss = zip(*data_set_one)
eatmap, xedges, yedges = np.histogram2d(x, y, weights=gauss, bins=100)
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

plt.clf()
plt.imshow(heatmap.T, extent=extent, origin='lower')
plt.title("Part A")
plt.show()

# Part B results
x, y, gauss = zip(*data_set_two)
eatmap, xedges, yedges = np.histogram2d(x, y, weights=gauss, bins=100)
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

plt.clf()
plt.imshow(heatmap.T, extent=extent, origin='lower')
plt.title("Part B")
plt.show()
