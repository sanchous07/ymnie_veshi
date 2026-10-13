import matplotlib.pyplot as plt
def plot_voltage_vs_time(time,voltage,max_voltage):
    plt.figure(figsize=(10,6))
    plt.plot(time,voltage)
    plt.ylabel("voltage")
    plt.xlabel('time')
    plt.xlim(0,3.0)
    plt.ylim(0,3.5)
    plt.grid()
    plt.show()

def plot_sampling_period_hist(time):
    sampling_periods=[]
    for i in range(len(time)-1):
        sampling_periods.append(time[i+1]-time[i])
    plt.figure(figsize=(10,6))
    plt.hist(sampling_periods)
    plt.xlabel('periods,s')
    plt.ylabel('count of izmerenia')
    plt.xlim(0.0,0.06)
    plt.ylim(0,1000)
    plt.grid()
    plt.show()