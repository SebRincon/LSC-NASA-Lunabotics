from machine import Pin
import time

def moveMotor(isForward):
    pinEnabled = Pin(23, Pin.OUT,value=0)
    pinStep = Pin(22, Pin.OUT)
    pinDirection = Pin(1, Pin.OUT)
    stepsPerRevolution = 50
    
    
    if isForward:
        pinDirection.on()
        print('Moving Forwards')
        for i in range(0,stepsPerRevolution):
            pinStep.on()
            time.sleep_ms(10)
            pinStep.off()
            time.sleep_ms(10)
        print('Done Moveing')
        time.sleep_ms(500)

    else:
        pinDirection.off()
        for i in range(0,stepsPerRevolution):
            pinStep.on()
            time.sleep_ms(10)
            pinStep.off()
            time.sleep_ms(10)
        time.sleep_ms(500)

while True:
    totalSteps = 0
    move = input('Move ?: y - n: ')
    if move == 'y':
        moveMotor(True)
        totalSteps = totalSteps + 50
        print('Total Steps: ' + totalSteps)