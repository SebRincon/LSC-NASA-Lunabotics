
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



def relay(isON):

    # ESP32 GPIO 26
    relay = Pin(23, Pin.OUT)


    if isON:
      # RELAY ON
      relay.value(0)
      
    else:
      # RELAY OFF
      relay.value(1)


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
        if _data == b'mt_on':
            relay(True)
        elif _data == b'mt_off':
            relay(False)
            
        
        