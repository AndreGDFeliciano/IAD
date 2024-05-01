import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from scipy.odr import ODR, Model, RealData



file_path      = 'dataset_2024-04-30 13:57:24.626902.txt'
file_path_UNIX = 'test_threshold_21_UNIX.txt'
file_path_34   = 'test_21_34.txt'

df_1    = pd.read_csv (file_path      , sep=' ')
df_UNIX = pd.read_csv (file_path_UNIX , sep=' ')
df_34   = pd.read_csv (file_path_34   , sep=' ')


s1_count    = df_1.iloc[:, 0].values.tolist()  #nº do evento
s1_UNIX_s   = df_1.iloc[:, 1].values.tolist()  #tempo do evento UNIX
s1_peak1_mv = df_1.iloc[:, 2].values.tolist()  #peak no detetor 1
s1_peak2_mv = df_1.iloc[:, 3].values.tolist()  #peak no detetor 2
s1_time_us  = df_1.iloc[:, 4].values.tolist()  #time from arduino us
s1_int_us   = df_1.iloc[:, 5].values.tolist()  #interval in us
s1_int_s    = [val*1E-6 for val in s1_int_us]  # transformar us em ms

UNIX_peak_mV = df_UNIX.iloc[:, 0].values.tolist()  #peak no detetor
UNIX_UNIX_s  = df_UNIX.iloc[:, 1].values.tolist()  #UNIX time s
UNIX_int_s   = df_UNIX.iloc[:, 2].values.tolist()  #interval s

s34_peak1_mV = df_34.iloc[:, 0].values.tolist()  #peak no detetor
s34_peak2_mV = df_34.iloc[:, 1].values.tolist()  #peak no detetor
s34_Ard_s    = df_34.iloc[:, 2].values.tolist()  #Ard time s useless
s34_int_us   = df_34.iloc[:, 3].values.tolist()  #interval time s
s34_int_s    = [val*1E-6 for val in s34_int_us]  # transformar us em s
s34_UNIX_s   = df_34.iloc[:, 4].values.tolist()  #UNIX s


def hist_exp(intervals):
    """Creates and histogram with the intervals

    Args:
        intervals (_type_): _description_
    """
    plt.xlabel("tempo entre det.(ms)")
    plt.ylabel("Nº contagens")
    #bins = int((max(intervals)-min(intervals))/1000000)
    plt.hist(intervals,100)
    plt.show()

def hist_exp_log(intervals):
    plt.xlabel("tempo entre det.(ms)")
    plt.ylabel("Nº contagens (log)")
    plt.yscale("log")
    #bins = int((max(intervals)-min(intervals))/10)
    plt.hist(intervals,11)
    plt.show()

def fit_exp_0(intervals):
    plt.xlabel("tempo entre det.(ms)")
    plt.ylabel("Nº contagens")
    bins = int((max(intervals)-min(intervals))/10000)
    y_list, x_list = np.histogram(intervals,12,
                                  (min(intervals),max(intervals)))
    center = (x_list[1]-x_list[0])/2
    x_list = [x_list[bin]+center for bin in range(len(x_list)-1)]
    y_list = list(y_list)
    x_err = [center*0.75] * len(x_list)
    y_err = [np.sqrt(y_list[bin]) for bin in range(len(y_list))]
    lin_data = RealData(x_list, y_list, sx=x_err, sy=y_err)
    plt.plot(x_list,y_list)
    plt.show()

def max_peak(peak1,peak2):
    if len(peak1) != len(peak2):
        raise ValueError("not the same length")
    peak_max = []
    for i in range(len(peak1)):
        if peak1[i] >= peak2[i]: peak_max.append(peak1[i])
        else: peak_max.append(peak2[i])
    bins= int((max(peak_max)-min(peak_max))/5)
    plt.xlabel("Tensão máxima (mV)")
    plt.ylabel("Nº contagens")
    plt.hist(peak_max,bins,[102,max(peak_max)])
    plt.show()

def max_peak_log(peak1,peak2):
    if len(peak1) != len(peak2):
        raise ValueError("not the same length")
    peak_max = []
    for i in range(len(peak1)):
        if peak1[i] >= peak2[i]: peak_max.append(peak1[i])
        else: peak_max.append(peak2[i])
    bins= int((max(peak_max)-min(peak_max))/5)
    plt.xlabel("Tensão máxima (mV)")
    plt.ylabel("Nº contagens")
    plt.yscale("log")
    plt.hist(peak_max,bins,[102,max(peak_max)])
    plt.show()

def UNIX_time(UNIX_times,window_s):
    bins = int((max(UNIX_times)-min(UNIX_times))/window_s)
    plt.hist(UNIX_times,bins)
    plt.show()

file_path = 'dataset_2024-04-29 20:30:52.492645.txt'
df_1 = pd.read_csv(file_path, sep=' ')

# Extracting data from the DataFrame
s1_int_us = df_1.iloc[:, 6].values.tolist()  # Column for interval in microseconds
s1_int_s  = [val * 1E-6 for val in s1_int_us]  # Convert microseconds to seconds

def exponential_func(p, x):
    """ Exponential decay function A * exp(-B * x) + C """
    A, B, C = p
    return A * B * np.exp(- x * B)

def fit_exp(intervals):
    # Histogram data
    y_list, x_edges = np.histogram(intervals, bins=50)
    x_list = 0.5 * (x_edges[1:] + x_edges[:-1])  # Calculate bin centers
    y_list = list(y_list)

    # Error estimations
    x_err = [0.5 * (x_edges[1] - x_edges[0])] * len(x_list)
    y_err = [np.sqrt(y) if y > 0 else 1 for y in y_list]

    # Prepare real data for ODR
    data = RealData(x_list, y_list, sx=x_err, sy=y_err)

    # Create a Model
    model = Model(exponential_func)

    # Set up ODR with the model and data
    odr = ODR(data, model, beta0=[900, 0.4, 0])

    # Run the regression
    output = odr.run()

    # Use the fitted parameters to plot the fitted curve
    x_fit = np.linspace(min(x_list), max(x_list), 1000)
    y_fit = exponential_func(output.beta, x_fit)

    plt.figure()
    plt.errorbar(x_list, y_list, yerr=y_err, xerr=x_err, fmt='o', label='Data')
    plt.plot(x_fit, y_fit, 'r-', label='Fit: A/B*exp(-x/B) + C')
    plt.xlabel("Time between detections (s)")
    plt.ylabel("Number of counts")
    plt.legend()

    # Printing the parameters and standard errors
    print("Fitted parameters: A = {:.2f}, B = {:.4f}, C = {:.2f}".format(*output.beta))
    print("Standard errors: σA = {:.2f}, σB = {:.4f}, σC = {:.2f}".format(*output.sd_beta))

    plt.show()

def hist_hourofday(data):
    """
    Makes an histogram by hour of the day
    Cumulative of the days recorded, and will cut so that we only have 24
    hour days.

    Warning: be careful with daylight saving time

    Args:
        filepath (string): path to file with the data to analyse

    """
    UNIX_first,UNIX_last = data[0],data[-1]
    date_0 = datetime.fromtimestamp(UNIX_first)
    date_last = datetime.fromtimestamp(UNIX_last)
    hour_0, day_0    = date_0.hour, date_0.day
    hour_last,day_last = date_last.hour, date_last.day
    n_days = (date_last - date_0).days
    hour_lim = hour_0 +1
    if hour_0 == 23:hour_lim = 0 #resolução do problema no caso de 23h

    start,finish,list_hour = False, False, []
    for UNIX in data:
        hour_UNIX = datetime.fromtimestamp(UNIX).hour
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
    # queremos a taxa horária, temos de dividir pelo número de dias
    plt.hist(list_hour,24)
    plt.show(block = True)

file_path = 'test_threshold_21_UNIX.txt'
df_1 = pd.read_csv(file_path, sep=' ')

# Extracting data from the DataFrame
s1_UNIX_s = df_1.iloc[:, 1].values.tolist()  # Column for interval in microseconds
#s1_int_s = [val * 1E-6 for val in s1_int_us]  # Convert microseconds to seconds

# Call the function with your data
#fit_exp(s1_int_s)
hist_exp(s34_int_s)
fit_exp(s34_int_s)
#hist_hourofday(s1_UNIX_s)
#UNIX_time(s1_UNIX_s,3600)
#hist_exp(s1_int_s)
#fit_exp(s1_int_s)