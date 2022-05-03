import os 
import network
import socket

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

    pinEnabled = Pin(23, Pin.OUT,value=0)
    pinStep = Pin(22, Pin.OUT)
    pinDirection = Pin(1, Pin.OUT)

    stepsPerRevolution = 200

    if isForward:
        pinDirection.on()

        for i in range(0,stepsPerRevolution):
            pinStep.on()
            time.sleep_ms(10)
            pinStep.off()
            time.sleep_ms(10)
    else:
        pinDirection.off()

        for i in range(0,stepsPerRevolution):
            pinStep.on()
            time.sleep_ms(10)
            pinStep.off()
            time.sleep_ms(10)    
                    
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