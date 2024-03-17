import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('ggplot') #Style
# Creating Dataframes
df_em = pd.read_csv('EJ200-1.txt', header=1, delimiter=',')
df_det = pd.read_csv('PDE4.txt', header=1, delimiter=',')

em_x  = df_em.iloc[:, 0].values.tolist()  #nº do evento
em_x  = [val + 380 for val in em_x]
em_y  = df_em.iloc[:, 1].values.tolist()  #tempo unix em s

det_x = df_det.iloc[:, 0].values.tolist()  #nº do evento
det_y = df_det.iloc[:, 1].values.tolist()  #tempo unix em s

rem = []
for lamb in range(len(det_x)):
    if det_x[lamb] > 100 and det_x[lamb] < 200:
        det_x[lamb] = det_x[lamb] + 300
        det_y[lamb] = det_y[lamb]/100
    else:
        rem.append(lamb)

rem.reverse()
for ind in rem:
    det_x.pop(ind)
    det_y.pop(ind)

# print(min(em_x)) # 397.6481 = 398
# print(max(em_x)) # 499.9981 = 500
# print(len(em_x)) # 206
# 500-398/206 = 0,5

em_x  = [(round(2*val)/2) for val in em_x]
integ_em = 0
for ind in range(1,len(em_x)):
    integ_em += em_y[ind]*(em_x[ind]-em_x[ind-1])
print(integ_em)


det_x = [(round(2*val)/2) for val in det_x]
#plt.scatter(em_x,em_y, label = "hist e plot")
#plt.scatter(det_x,det_y, label = "hist e plot")
#plt.show(block=False)

set_det = {val for val in det_x}


mult_x = []
mult_y = []
for ind in range(len(em_x)):
    if em_x[ind] in set_det:
        mult_x.append(em_x[ind])
        temp_mult_y = em_y[ind]
        i2 = 1
        while em_x[ind] == em_x[ind+i2]:
            temp_mult_y += em_y[ind]
            i2 += 1
        mult_y.append((temp_mult_y/i2)*det_y[det_x.index(em_x[ind])])

integ_mult = 0
for ind in range(1,len(mult_x)):
    integ_mult += mult_y[ind]*(mult_x[ind]-mult_x[ind-1])
print(integ_mult)
print(integ_mult/integ_em*100) # 39,34 %

plt.scatter(mult_x,mult_y, label = "hist e plot")
plt.show(block=True)
