import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

class R2R_DAC:
    def __init__(self, gpio_bits, d_range, verbose = False): 
        self.gpio_bits=gpio_bits
        self.d_range=d_range
        self.verbose=verbose

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits,GPIO.OUT, initial=0)

    def deinit(self):
        GPIO.output(self.gpio_bits,0)
        GPIO.cleanup()

    def set_number(self,n):
        GPIO.output(self.gpio_bits,[int(el)for el in bin(n)[2:].zfill(8)])

    def set_voltage(self, voltage):
        if not (0.0<=voltage<=self.d_range):
            print("Напряжение выходит за динамический диапозон ЦАП (0.0 - {d_range:.2f} B)")
            print("Устанавливаем 0.0 В")
            return 0
        v=int(voltage/self.d_range*255)
        GPIO.output(self.gpio_bits,[int(el)for el in bin(v)[2:].zfill(8)])

if __name__=="__main__":
    try:
        dac=R2R_DAC([16,20,21,25,26,17,27,22],3.183,True)

        while True:
            try:
                voltage=float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте еще раз\n")
    finally:
        dac.deinit()
