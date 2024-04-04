import numpy  as np
import matplotlib.pyplot as plt
from datetime import datetime as date

np.random.seed(123)

file_path = 'test_data.txt'
f = open(file_path,"w")

UNIX_time = 1712063008
# There is a problem here with the datetime, because of the daylight saving
# time change.
rate_s = 0.7 # rate de muões s-1
rate_param_s = 1 / rate_s
rate_param_s2 = 1/ 0.9
n_mu = 1000000

# 60480 equivalente a um dia em tempo

def dados_2val(n_mu,rate_param_s,rate_param_s2,time):
    file_path = 'test_data.txt'
    f = open(file_path,"w")
    time_int_l = []
    UNIX_time = time
    rand_exp  = np.random.exponential(rate_param_s,n_mu)
    rand_exp2 = np.random.exponential(rate_param_s2,n_mu)
    for i in range(n_mu):
        if date.fromtimestamp(UNIX_time).hour in {7,8,9,10,11,12,13,14,15,16}:
            time_int = rand_exp2[i]
        else:
            time_int = rand_exp[i]
        time_int_l.append(time_int)
        UNIX_time += time_int
        f.write(f"{i},{int(UNIX_time)}\n")
    n_bins = int(max(time_int_l))
    plt.hist(time_int_l,n_bins)
    plt.show()

def dados_sin_val(n_mu,time,rate_s = 0.7):
    file_path = 'test_data.txt'
    f = open(file_path,"w")
    rate_s = 0.7
    rate_param_s = 1 / rate_s
    time_int_l = []
    UNIX_time = time
    for i in range(n_mu):
        time_int = np.random.exponential(1/
        (rate_s+0.2*np.sin(np.pi * date.fromtimestamp(UNIX_time).hour/23)))
        time_int_l.append(time_int)
        UNIX_time += time_int
        f.write(f"{i},{int(UNIX_time)}\n")
    n_bins = int(max(time_int_l))
    plt.hist(time_int_l,n_bins)
    plt.show()

def cdf_exponential(rate_s,x):
    return 1-np.exp(-rate_s*x)

min_dt = 0.1 # in seconds
print(cdf_exponential(rate_s,min_dt))


exp_value = []
exp_x = []
for i in range(0,80,1):
    exp_x.append(i*0.1)
    exp_value.append(1/rate_param_s*np.exp(-i*0.1/rate_param_s)*n_mu)



# dados_sin_val(n_mu,UNIX_time,rate_s)


#n_bins = int(max(time_int_l))
#plt.plot(exp_x , exp_value)
#plt.hist(time_int_l,n_bins)
#plt.show()