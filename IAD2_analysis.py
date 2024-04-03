import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.odr import ODR, Model, RealData
import time
from datetime import datetime as date
from datetime import timedelta as dt


filename = 'test_data.txt'
df_1 = pd.read_csv('test_data.txt', sep=',')

s1_num    = df_1.iloc[:, 0].values.tolist()  #nº do evento
s1_t_s    = df_1.iloc[:, 1].values.tolist()  #tempo unix em s
s1_t_date = [date.fromtimestamp(val).hour for val in s1_t_s]
n_days = (date.fromtimestamp(s1_t_s[-1]) - date.fromtimestamp(s1_t_s[0])).days
print("timedelta =",n_days)
#print(date.fromtimestamp(s1_t_s[0]))
#print(date.fromtimestamp(s1_t_s[0]).hour)
#print(date.fromtimestamp(s1_t_s[-1]))
#print(date.fromtimestamp(s1_t_s[-1]).hour)
s1_t_s = [val - s1_t_s[0] for val in s1_t_s]

dif_s = s1_t_s[-1] - s1_t_s[0]
print(dif_s) # 14104

#plt.hist(s1_t_date,24)
plt.show(block = False)

rate = s1_num[-1] / dif_s

def read_file(filepath):
    """Reads the file and returns a list of 2 lists

    Args:
        filepath (string): path to file with the data to analyse
    Returns:
        read_file[0] (list): list of values in first column
        read_file[1] (list): list of values in second column
    """
    pd.read_csv(filepath, sep = ",")
    s1_num    = df_1.iloc[:, 0].values.tolist()  #nº do evento
    s1_t_s    = df_1.iloc[:, 1].values.tolist()  #tempo unix em s
    return [s1_num,s1_t_s]

def muon_rate(filepath):
    data = read_file(filepath)
    t0 = data[1][0]
    dif_s = data[1][-1] - t0
    print(data[0][-1]/dif_s)
    return data[0][-1]/dif_s

def hist_time(filepath, timeint=False):
    """
    Makes an histogram, asks for the time interval desired
    y_axis represents the events in that time interval
    x_axis will start at 0 and will be counting the time intervals


    Args:
        filepath (string): path to file with the data to analyse

    """
    data = read_file(filepath)
    if not timeint:
        timeint = int(input("Select the number of seconds per bin:"))
    t0 = data[1][0]
    dif_s = data[1][-1] - t0
    n_bins = dif_s//timeint
    data[1] = [(t-t0)/timeint for t in data[1]]
    plt.hist(data[1], n_bins)
    plt.show()

def hist_hourofday(filepath):
    """
    Makes an histogram by hour of the day
    Cumulative of the days recorded, and will cut so that we only have 24
    hour days.

    Warning: be careful with daylight saving time

    Args:
        filepath (string): path to file with the data to analyse

    """
    data = read_file(filepath)
    UNIX_first,UNIX_last = data[1][0],data[1][-1]
    date_0 = date.fromtimestamp(UNIX_first)
    date_last = date.fromtimestamp(UNIX_last)
    hour_0, day_0    = date_0.hour, date_0.day
    hour_last,day_last = date_last.hour, date_last.day
    n_days = (date_last - date_0).days
    hour_lim = hour_0 +1
    if hour_0 == 23:hour_lim = 0 #resolução do problema no caso de 23h

    start,finish,list_hour = False, False, []
    for UNIX in data[1]:
        hour_UNIX = date.fromtimestamp(UNIX).hour
        if not start and hour_UNIX != hour_0:
                start = True
        if start:
            list_hour.append(hour_UNIX)
        # currently only uses 1 day for normalizing purposes
        if UNIX > UNIX_first + 82600 and hour_UNIX == hour_lim:
            break
    """
    avoiding start/stop bias there are 2 ways we can go about this
    1. We choose the date in the way that it is simply 24 hours and it
    becomes direct
    2. We divide it by the number of days with each hour.
    """
    # y_list,x_list = np.histogram(list_hour,24,[0,24])
    # y_list = [val/n_days for val in y_list]
    # x_list = x_list[:-1]
    # plt.plot(x_list,y_list)
    # queremos a taxa horária, temos de dividir pelo número de dias
    plt.hist(list_hour,24)
    plt.show(block = False)

def hist_hourofday_average(filepath):
    data = read_file(filepath)
    UNIX_first,UNIX_last = data[1][0],data[1][-1]
    date_0 = date.fromtimestamp(UNIX_first)
    date_last = date.fromtimestamp(UNIX_last)
    hour_0 = date_0.hour
    n_days = (date_last - date_0).days
    hour_lim = hour_0 + 1
    if hour_0 == 23: hour_lim = 0 #resolução do problema no caso de 23h

    start,list_hour = False, []
    for UNIX in data[1]:
        hour_UNIX = date.fromtimestamp(UNIX).hour
        if not start and hour_UNIX != hour_0:
                start = True
        if start:
            list_hour.append(hour_UNIX)
        if UNIX > UNIX_last - 86400 and hour_UNIX == hour_lim:
            break
    y_list,x_list = np.histogram(list_hour,24,[0,24])
    y_list = [val//n_days for val in y_list]

    # divide to obtain the average hourly rate
    x_list = x_list[:-1] # x_list comes with 1 more arguments
    for i in range(len(x_list)): print(x_list[i],",",y_list[i])
    plt.plot(x_list,y_list)
    plt.show(block= True)


muon_rate(filename)
hist_time(filename,3600)
#hist_hourofday(filename)
#hist_hourofday_average(filename)