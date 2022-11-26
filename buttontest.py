import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    if (not GPIO.input(5)):
        print("pressed")
        break

GPIO.cleanup()