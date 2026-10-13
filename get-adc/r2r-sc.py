import r2r_adc
import time
import adc_plot

voltage_values=[]
time_values=[]
duration=15.0
compare_time=0.0001
d_range=3.3

try:
    r2r=r2r_adc.R2R_ADC(d_range, compare_time)
    t0=time.time()
    while time.time()-t0<duration:
            voltage=r2r.get_sc_voltage()
            voltage_values.append(voltage)
            time_values.append(time.time()-t0)
    adc_plot.plot_voltage_vs_time(time_values,voltage_values,d_range)
    adc_plot.plot_sampling_period_hist(time_values)
finally:
    r2r.deinit()