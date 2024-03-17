import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

f = open("ploteff_2D.txt","w+")

xy_tot = [[],[],[]]
xy_det1 = [0,-3]
xy_det2 = [0, 3]

def dist(coord,coord2):
    return np.sqrt((coord[0]-coord2[0])**2 + (coord[1]-coord2[1])**2)

def find_angle(a,b):
    cos_C = (a**2 + b**2 - 6**2) / (2 * a * b)
    return np.arccos(cos_C)

for x_ind in range(1,101):
    for y_ind in range(-49,51):
        xy_coord = (x_ind-0.5,y_ind-0.5)
        dist1  = dist(xy_coord,xy_det1)
        dist2  = dist(xy_coord,xy_det2)
        xy_eff = find_angle(dist1,dist2)/(2*np.pi)
        if xy_eff > 0.2:
            xy_tot[0].append(x_ind-0.5)
            xy_tot[1].append(y_ind-0.5)
            xy_tot[2].append(xy_eff)

        #f.write(str(x_ind-0.5)+","+str(y_ind-0.5)+", "+str(xy_eff)+"\n")

plt.scatter(xy_tot[0], xy_tot[1], c=xy_tot[2], cmap='plasma',
            norm=colors.LogNorm(vmin=0.2, vmax=0.5))
plt.show()

f.close()









