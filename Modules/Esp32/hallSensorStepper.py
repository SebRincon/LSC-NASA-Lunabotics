import os 
import network
import socket
import eps32

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('ciscosb1', 'rimor1234')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

def moveMotor(isForward):
    from machine import Pin
    import time
    import esp32

    pinEnabled = Pin(23, Pin.OUT,value=0)
    pinStep = Pin(22, Pin.OUT)
    pinDirection = Pin(1, Pin.OUT)
    stepsPerRevolution = 20
    
    value = esp32.hall_sensor()
    print(value)
    
    if isForward:
        pinDirection.on()
        while esp32.hall_sensor() < 50:
            
            for i in range(0,stepsPerRevolution):
                pinStep.on()
                time.sleep_ms(10)
                pinStep.off()
                time.sleep_ms(10)
                
            
            print("SLEEP")
            time.sleep_ms(500)
    else:
        pinDirection.off()
        while esp32.hall_sensor() > -20:

            for i in range(0,stepsPerRevolution):
                pinStep.on()
                time.sleep_ms(10)
                pinStep.off()
                time.sleep_ms(10)
                
            value = esp32.hall_sensor()
            print(value)
            time.sleep_ms(500)

                    
def socketConnection():
    data = b'fr'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("data is type {}".format(type(data)))

    sock.connect(('192.168.1.101', 5000))
    
    _resp = sock.recv(1024)
    print(_resp)

    sock.send(data)
    _resp = sock.recv(1024)
    print(_resp)
    
    while True:
        _data = sock.recv(1024)
        print(_data[0:2])
        if _data == b'fr_bk':
            print('Moving Motor')
            moveMotor(False)
        elif _data == b'fr_fw':
            moveMotor(True)
    sock.close()
    

do_connect()
socketConnection()