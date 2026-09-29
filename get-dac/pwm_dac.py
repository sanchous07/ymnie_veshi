import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, d_range, verbose = False): 
        self.gpio_bits=gpio_pin
        self.pwm_frequency=pwm_frequency
        self.d_range=d_range
        self.verbose=verbose

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial=0)

        global pwm
        pwm=GPIO.PWM(self.gpio_bits,self.pwm_frequency)

    def deinit(self):
        GPIO.output(self.gpio_bits,0)
        GPIO.cleanup()
        pwm.stop()

    def set_voltage(self, voltage):
        if not (0.0<=voltage<=self.d_range):
            print("Напряжение выходит за динамический диапозон ЦАП (0.0 - {d_range:.2f} B)")
            print("Устанавливаем 0.0 В")
        else:
            k=voltage/self.d_range*100
            pwm.start(k)

        return None
                   

if __name__=="__main__":
    try:
        dac=PWM_DAC(12, 500, 3.290, True)

        while True:
            try:
                voltage=float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте еще раз\n")
    finally:
        dac.deinit()