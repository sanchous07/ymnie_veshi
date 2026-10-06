import r2r_dac as r2r
import signal_generator as sg
import time

amplitude=3.2
sig_freq=10
sampling_freq=1000
pins=[16,20,21,25,26,17,27,22]
d_range=3.3

try:
    dac=r2r.R2R_DAC(pins, d_range)

    while True:
        try:
            voltage=sg.get_sin_wave_amplitude(sig_freq, time.time())*amplitude
            sg.wait_for_sampling_period(sampling_freq)
            dac.set_voltage(voltage)
        
        except ValueError:
            print("Выход за границы диапазона")
finally:
    dac.deinit()