import time

def get_trgl_amplitude(freq,time):
    return freq*abs(1/freq-2*(time%(1/freq)))

def wait_for_sampling_period(sampling_frequency):
    time.sleep(1/sampling_frequency)
    return None