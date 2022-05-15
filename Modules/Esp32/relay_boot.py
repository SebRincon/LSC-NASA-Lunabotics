
from machine import Pin
from time import sleep


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



def relay(isON, isForward):

    # ESP32 GPIO 26
    relay = Pin(23, Pin.OUT)
    _r1_1= Pin(13, Pin.OUT) # Negative Secondary
    _r1_2= Pin(12, Pin.OUT) # Positive Secondary
    _r2_1= Pin(23, Pin.OUT) # Positive Main
    _r2_2= Pin(22, Pin.OUT) # Negative Main
    
    _r2_1.value(1)
    _r2_2.value(1)
    _r1_1.value(1)
    _r1_2.value(1)


    if isON:
        if isForward:
            _r1_1.value(0) #OFF
            _r1_2.value(0)
            
            _r2_1.value(1) #ON
            _r2_2.value(1)
        else:
            _r2_1.value(0) #OFF
            _r2_2.value(0) 
            
            _r1_1.value(1) #ON
            _r1_2.value(1)
      
    else:

        _r2_1.value(1)
        _r2_2.value(1)
        _r1_1.value(1)
        _r1_2.value(1)



def socketConnection():
    data = b'mt'
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
        if _data == b'mt_on_fw':
            relay(True, True)
        elif _data == b'mt_on_bk':
            relay(True, False)
        elif _data == b'mt_off':
            relay(False, False)
            
        
        