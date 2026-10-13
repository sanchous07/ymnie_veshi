import RPi.GPIO as GPIO
import time

def dec_to_bin(n):
    return [int(el) for el in bin(n)[2:].zfill(8)]
class R2R_ADC:
    def __init__(self, d_range, compare_time=0.01, verbose=False):
        self.d_range=d_range
        self.verbose=verbose
        self.compare_time=compare_time

        self.bits_gpio=[26,20,19,16,13,12,25,11]
        self.comp_gpio=21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio,GPIO.OUT,initial=0)
        GPIO.setup(self.comp_gpio,GPIO.IN)

    def deinit(self):
        GPIO.output(self.bits_gpio,0)
        GPIO.cleanup()

    def number_to_dac(self,n):
        if n>=2**len(self.bits_gpio):
            n=2**len(self.bits_gpio)-1
        if n<0:
            n=0
        
        n_bin=dec_to_bin(n)
        n_bin=[0]*(len(self.bits_gpio)-len(n_bin))+n_bin

        GPIO.output(self.bits_gpio,n_bin)
    
    def sequential_counting_adc(self):
        n=0
        self.number_to_dac(n)
        while not(GPIO.input(self.comp_gpio)) and n<=2**len(self.bits_gpio):
            self.number_to_dac(n)
            time.sleep(self.compare_time)
            n+=1
        return n
    def get_sc_voltage(self):
        n=self.sequential_counting_adc()
        return self.d_range*n/(2**len(self.bits_gpio))

    def successive_approximation_adc(self):
        GPIO.output(self.bits_gpio,0)
        bits_values=[0]*len(self.bits_gpio)
        for i in range(len(self.bits_gpio)):
            bits_values[i]=1
            GPIO.output(self.bits_gpio,bits_values)
            time.sleep(self.compare_time)
            if GPIO.input(self.comp_gpio)==1:
                bits_values[i]=0
        return int(''.join(list(map(str,bits_values))),2)

    def get_sar_voltage(self):
        n=self.successive_approximation_adc()
        return self.d_range*n/2**len(self.bits_gpio)

if __name__=='__main__':
    try:
        r2r=R2R_ADC(3.3)

        while True:
            # voltage=r2r.get_sc_voltage()
            voltage=r2r.get_sar_voltage()
            if voltage!=0:
                print(voltage)
            
    finally:
        r2r.deinit()

    
