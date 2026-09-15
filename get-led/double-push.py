import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

leds=[16,12,25,17,27,23,22,24]
GPIO.setup(leds, GPIO.OUT)
GPIO.output(leds,0)
sleep_time=0.2

up=9
down=10
GPIO.setup(up,GPIO.IN)
GPIO.setup(down,GPIO.IN)

num=0
def dec2bin(value):
    return [int(element) for element in bin(value)
[2:].zfill(8)]

while True:
    if GPIO.input(up) and GPIO.input(down):
        num=255
        time.sleep(sleep_time)
    elif GPIO.input(up):
        num=num+1
        if num==256:
            print("NELZYA BOLSHE")
            GPIO.output(leds,1)
            time.sleep(0.1)
            GPIO.output(leds,0)
            num=255
        print(num,dec2bin(num))
        GPIO.output(leds, dec2bin(num))
        time.sleep(sleep_time)
    elif GPIO.input(down):
        num=num-1
        if num==-1:
            print("NELZYA MENSHE")
            GPIO.output(leds,1)
            time.sleep(0.1)
            GPIO.output(leds,0)
            num=0
        print(num,dec2bin(num))
        time.sleep(sleep_time)
        GPIO.output(leds, dec2bin(num))