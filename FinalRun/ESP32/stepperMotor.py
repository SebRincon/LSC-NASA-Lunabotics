import os 
import network
import socket
import esp32
import json

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('ciscosb1', 'rimor1234')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

def moveMotor(isForward, stopMotor = False):
    from machine import Pin
    import time


    pinEnabled = Pin(23, Pin.OUT,value=0)
    pinStep = Pin(22, Pin.OUT)
    pinDirection = Pin(1, Pin.OUT)
    stepsPerRevolution = 20
    
    value = esp32.hall_sensor()
    print(value)

    if stopMotor:
        pinStep.off()
    
    elif isForward:
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
    # data = b'bk'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.connect(('192.168.1.101', 5001))
    
    _resp = sock.recv(1024)
    print(_resp)

    sock.send(data)
    _resp = sock.recv(1024)

    print(_resp.decode('utf-8'))
    
    if _resp.decode('utf-8') == 'fr':
        while True:
            data = sock.recv(1024)
            _data = data.decode('utf-8')
            print(data)
            print(' ')
            if _data == 'fr_fw':
                print('Moving Motor')
                moveMotor(True)
            elif _data == 'fr_bk':
                moveMotor(False)

            else:
                moveMotor(False, True)
    elif _resp.decode('utf-8') == 'bk':
        while True:
            data = sock.recv(1024)
            _data = data.decode('utf-8')
            print(data)
            if _data == 'bk_fw':
                print('Moving Motor')
                moveMotor(True)
            elif _data == 'bk_bk':
                moveMotor(False)
    sock.close()
    

do_connect()
socketConnection()