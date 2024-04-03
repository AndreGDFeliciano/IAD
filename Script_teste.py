import numpy  as np
import matplotlib.pyplot as plt
from datetime import datetime as date

np.random.seed(123)

file_path = 'test_data.txt'
f = open(file_path,"w")

time = 1712063008
# There is a problem here with the datetime, because of the daylight saving
# time change.
rate_s = 0.7 # rate de muões s-1
rate_param_s = 1 / rate_s
rate_param_s2 = 1/ 0.9
time_int_l = []
n_mu = 1000000
rand_exp  = np.random.exponential(rate_param_s,n_mu)
rand_exp2 = np.random.exponential(rate_param_s2,n_mu)
# 60480 equivalente a um dia em tempo
for i in range(n_mu):
    if date.fromtimestamp(time).hour in {7,8,9,10,11,12,13,14,15,16}:
        time_int = rand_exp2[i]
    else:
        time_int = rand_exp[i]
    time_int_l.append(time_int)
    time += time_int
    f.write(f"{i},{int(time)}\n")

exp_value = []
exp_x = []
for i in range(0,80,1):
    exp_x.append(i*0.1)
    exp_value.append(1/rate_param_s*np.exp(-i*0.1/rate_param_s)*n_mu)

n_bins = int(max(time_int_l))
plt.plot(exp_x , exp_value)
plt.hist(time_int_l,n_bins)
plt.show()