import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

exits=[16, 20, 21, 25, 26, 17, 27, 22]
GPIO.setup(exits, GPIO.OUT)
GPIO.output(exits, 0)

d_range=3.3
def voltage_to_number(voltage):
    if not (0.0<=voltage<=d_range):
        print("Напряжение выходит за динамический диапозон ЦАП (0.0 - {d_range:.2f} B)")
        print("Устанавливаем 0.0 В")
        return 0
    return int(voltage/d_range*255)
def number_to_dac(n):
    b=[int(el)for el in bin(n)[2:].zfill(8)]
    GPIO.output(exits,b)
    return 0

try:
    while True:
        try:
            voltage=float(input("Введите напряжение в Вольтах: "))
            number=voltage_to_number(voltage)
            number_to_dac(number)

        except ValueError:
            print("Вы ввели не число. Попробуйте еще раз\n")
finally:
    GPIO.output(exits,0)
    GPIO.cleanup()