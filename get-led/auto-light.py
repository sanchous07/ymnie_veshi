import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

led=26
GPIO.setup(led,GPIO.OUT)

fototranz=6
GPIO.setup(fototranz,GPIO.IN)

while True:
    GPIO.output(led, not(GPIO.input(fototranz)))
