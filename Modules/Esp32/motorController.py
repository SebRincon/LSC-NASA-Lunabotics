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
    
    
    
    
def moveStepper(isForward):
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

def moveMotor(isForward):
    from machine import Pin
    from time import sleep

    IN1 = Pin(26,Pin.OUT)
    IN2 = Pin(25,Pin.OUT)
    IN3 = Pin(33,Pin.OUT)
    IN4 = Pin(32,Pin.OUT)

    pins = [IN1, IN2, IN3, IN4]

    forwards = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
    backwards = [[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,0,0,0]]
    

    for i in range(15):
        if isForward:
            for step in forwards:
                for i in range(len(pins)):
                    pins[i].value(step[i])
                    sleep(0.001)
        else:
            for step in backwards:
                for i in range(len(pins)):
                    pins[i].value(step[i])
                    sleep(0.001)
                    
def socketConnection():
    data = b'fr'
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


