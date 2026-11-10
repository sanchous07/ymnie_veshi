import numpy as np
import rc_plot 

data=np.loadtxt('data.csv',
            delimiter=',',
            skiprows=1,
            encoding='utf-8')

time=data[:,0].astype(float)
voltage=data[:,1].astype(float)
d_range=10

rc_plot.plot_voltage_vs_time(time,voltage,d_range)

