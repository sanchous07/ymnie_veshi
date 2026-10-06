import pwm_dac as pwm
import signal_generator as sg 
import time

amplitude=3.2
pwm_freq=500
sig_freq=10
sampling_freq=1000
pin=12
d_range=3.3

try:
    dac=pwm.PWM_DAC(pin,pwm_freq,d_range)

    while True:
        try:
            voltage=sg.get_sin_wave_amplitude(sig_freq, time.time())*amplitude
            sg.wait_for_sampling_period(sampling_freq)
            dac.set_voltage(voltage)

        except ValueError:
            print("Выход за границы диапазона")
    
finally:
    dac.deinit()