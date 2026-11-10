import matplotlib.pyplot as plt
import numpy as np
def plot_voltage_vs_time(time,voltage,max_voltage):
    plt.figure(figsize=(10,6))
    plt.plot(time,voltage)
    plt.ylabel("voltage")
    plt.xlabel('time')
    plt.xlim(0,15)
    plt.ylim(0,max_voltage*1.2)
    plt.grid()
    plt.savefig('rc_plot.png', dpi=300)

def grafik_voltage(time, voltage, max_voltage):
    data=np.column_stack((time,voltage))
    np.savetxt('data.csv',
                data,
                delimiter=',',
                fmt='%4f',
                header='time [s], voltage [v]',
                comments='',
                encoding='utf-8')
    