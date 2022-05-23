import os 
import socket
import json
import time
import network
from machine import Pin

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
    pinEnabled = Pin(23, Pin.OUT,value=0)
    pinStep = Pin(22, Pin.OUT)
    pinDirection = Pin(1, Pin.OUT)
    stepsPerRevolution = 100
    
    if stopMotor:
        pinStep.off()
    
    elif isForward:
        pinDirection.on()
        for i in range(0,stepsPerRevolution):
            pinStep.on()
            time.sleep_ms(10)
            pinStep.off()
            time.sleep_ms(10)
        time.sleep_ms(500)

    else:
        pinDirection.off()
        for i in range(0,stepsPerRevolution):
            pinStep.on()
            time.sleep_ms(10)
            pinStep.off()
            time.sleep_ms(10)
        time.sleep_ms(500)

def socketConnection():
    data = 'fr'
    # data = b'bk'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.connect(('192.168.1.101', 5001))
    
    #! 1 Connection
    _resp = sock.recv(1024)
    print(_resp)

    #! 2 Feedback
    sock.send(data)
    _resp = sock.recv(1024)
    
    if _resp.decode('utf-8') == 'fr':
        print('Connection Established')
        while True:
            #! Loop
            data = sock.recv(1024)
            _data = data.decode('utf-8')
            #? Forwards
            if _data == 'fr_fw':
                print('Moving Motor')
                moveMotor(True)

            #? Backwards
            elif _data == 'fr_bk':
                moveMotor(False)

            #? Stop
            else:
                moveMotor(False, True)

    elif _resp.decode('utf-8') == 'bk':
        print('Connection Established')
        while True:
            #! Loop
            data = sock.recv(1024)
            _data = data.decode('utf-8')
            #? Forwards
            if _data == 'bk_fw':
                print('Moving Motor')
                moveMotor(True)
            #? Backwards
            elif _data == 'bk_bk':
                moveMotor(False)
            #? Stop
            else:
                moveMotor(False, True)    

do_connect()
socketConnection()