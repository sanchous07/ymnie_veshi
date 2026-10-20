import mcp3021_driver as mcp3021
import adc_plot
import time

voltage_values=[]
time_values=[]
duration=15.0
compare_time=0.0001
d_range=3.3

mcp=mcp3021.MCP3021(d_range)

try:
    t0=time.time()
    while time.time()-t0<duration:
            voltage=mcp.get_voltage()
            voltage_values.append(voltage)
            time_values.append(time.time()-t0)
    adc_plot.plot_voltage_vs_time(time_values,voltage_values,d_range)
    adc_plot.plot_sampling_period_hist(time_values)
finally:
    mcp.deinit()