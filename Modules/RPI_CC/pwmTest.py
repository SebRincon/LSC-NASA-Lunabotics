import RPi.GPIO as io

io.setmode(io.BOARD) # GPIO Settings
io.setup(33,io.OUT) # Use pin 12 as signal -> white cable to pin 12

pwmController = io.PWM(33,100) # Setting pin 12 as PWM pin and frequency to 100
pwmController.start(20) # Start motor at 20

stop = False # Stop Variable 



while(stop != True):
    #Manage Dutycycle speed & Direction
    dutycycle = input("Enter a duty cycle / speed: ")

    if int(dutycycle) == 0:
        stop = True
    try:
        pwmController.ChangeDutyCycle(int(dutycycle))
    except:
        print("PASS")
io.cleanup()
print('EXIT')
