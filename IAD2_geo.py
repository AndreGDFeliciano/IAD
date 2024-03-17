import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors



xy_tot = [[],[],[]]
xy_det1 = [0,-30]
xy_det2 = [0, 30]

def dist(coord,coord2):
    return np.sqrt((coord[0]-coord2[0])**2 + (coord[1]-coord2[1])**2)

def find_angle(a,b):
    cos_C = (a**2 + b**2 - 60**2) / (2 * a * b)
    arccos = np.arccos(cos_C)
    np.arccos()
    return arccos
#2D
"""
area = 1e6
integ_geo = 0
for x_ind in range(1,1001):
    for y_ind in range(-499,501):
        xy_coord = (x_ind-0.5,y_ind-0.5)
        dist1  = dist(xy_coord,xy_det1)
        dist2  = dist(xy_coord,xy_det2)
        xy_eff = find_angle(dist1,dist2)*20000*0.3934261625894686/\
                                            (2*np.pi)
        if xy_eff > 60:
            xy_tot[0].append(xy_coord[0])
            xy_tot[1].append(xy_coord[1])
            xy_tot[2].append(xy_eff)



        #f.write(str(xy_coord[0])+","+str(xy_coord[1])+", "+str(xy_eff)+"\n")

plt.scatter(xy_tot[0], xy_tot[1], c=xy_tot[2], cmap='plasma',
            norm=colors.LogNorm(vmin=1, vmax=4000))
plt.show()
"""

## Monte Carlo
dim = 100
n_phot = 4000 # 20000*0.3934*0.5
xyz_eff = [[],[],[],[]]
muon_det = 0
max_dist = np.sqrt(dim**2+(dim*0.53)**2+(dim*0.1)**2)
print("max_dist=", max_dist) #dim*1.1361778029868388
xy0_det = [[],[]]

for z_ind in range(dim):
    for y_ind in range(int(dim*-0.5),int(dim*0.5)):
        photon_det = 0
        for photon in range(n_phot):
            xyz_coord = (0,y_ind+0.5,z_ind+0.5)
            theta = np.random.uniform(np.pi/2,np.pi)
            phi   = np.random.uniform(0,2*np.pi)
            vector = (np.sin(theta)*np.cos(phi), # x
                      np.sin(theta)*np.sin(phi), # y
                      np.cos(theta))             # z
            lamb = - xyz_coord[2]/vector[2]
            #print(lamb)
            xy0_coord = [0,0]
            xy0_coord[0] = xyz_coord[0]+lamb*vector[0]
            xy0_coord[1] = xyz_coord[1]+lamb*vector[1]
            if  lamb < max_dist and\
                xy0_coord[0]<  dim*0.03 and\
                xy0_coord[0]> -dim*0.03 and\
                xy0_coord[1]<  dim*0.03 and\
                xy0_coord[1]> -dim*0.03:
                photon_det +=1
                #xy0_det[0].append(xy0_coord[0])
                #xy0_det[1].append(xy0_coord[1])

        if photon_det:
                photon_eff = photon_det/n_phot
                xyz_eff[0].append(xyz_coord[0])
                xyz_eff[1].append(xyz_coord[1])
                xyz_eff[2].append(xyz_coord[2])
                xyz_eff[3].append(photon_eff)
                if photon_det> 10:
                    muon_det +=1

print(muon_det/dim**2)



plt.scatter(xyz_eff[1], xyz_eff[2], c=xyz_eff[3], cmap='plasma',
            norm=colors.LogNorm(vmin=0.00025, vmax=1))

#plt.scatter( xy0_det[0],xy0_det[1])

plt.ylabel("z")
plt.xlabel("y")

plt.show()
# geo_eff = 0.969

