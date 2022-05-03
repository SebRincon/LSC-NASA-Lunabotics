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

    pinEnabled = Pin(5, Pin.OUT,value=0)
    pinStep = Pin(4, Pin.OUT)
    pinDirection = Pin(0, Pin.OUT)

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
    data = b'bk'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("data is type {}".format(type(data)))

    sock.connect(('192.168.1.100', 5011))
    
    _resp = sock.recv(1024)
    print(_resp)

    sock.send(data)
    _resp = sock.recv(1024)
    print(_resp)
    
    while True:
        _data = sock.recv(1024)
        print(_data[0:2])
        if _data == b'bk_bk':
            print('Moving Motor')
            moveMotor(False)
        elif _data == b'bk_fw':
            moveMotor(True)
            
        
        
    
    
    sock.close()

    

def starWars():
    addr_info = socket.getaddrinfo("towel.blinkenlights.nl", 23)
    addr = addr_info[0][-1]
    s = socket.socket()
    s.connect(addr)
    
    while True:
        data = s.recv(500)
        print(str(data, 'utf8'), end='')

do_connect()
socketConnection()
