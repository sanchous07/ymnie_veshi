import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

led=26
GPIO.setup(led,GPIO.OUT)
knopka=13

GPIO.setup(knopka, GPIO.IN)
status=0
while True:
    if GPIO.input(knopka):
        status=not status
        GPIO.output(led,status)
        time.sleep(0.2)