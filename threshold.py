import serial
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import time

arduino=serial.Serial(port="/dev/cu.usbmodemF412FA75E7882",baudrate=9600)


file_path = 'test_threshold.txt'


t_start__s = datetime.datetime.timestamp(datetime.datetime.now())
t_stop__s = datetime.datetime.timestamp(datetime.datetime.now())
t_dif__s = t_stop__s - t_start__s
print(t_dif__s)

file = open(file_path, "w")
while(t_stop__s - t_start__s < 50):
    read = arduino.readline().decode("UTF-8").rstrip()
    file.write(read + "\n")
    if not ((t_stop__s - t_start__s) % 20):
        file.flush()
    t_stop__s = datetime.datetime.timestamp(datetime.datetime.now())

file.flush()
file.close()


# df_1 = pd.read_csv (file_path, sep=' ')

# s1_PIN = df_1.iloc[:, 0].values.tolist()  #nº do evento
# s1_threshold  = df_1.iloc[:, 1].values.tolist()
# s1_out  = df_1.iloc[:, 1].values.tolist()
# s1_out = [val*4 for val in s1_out]
#for pin in range(len(s1_PIN)):
#    if s1_PIN(pin) = 15:
#        s1_threshold_out =
#plt.hist(s1_in,9)
#plt.show()