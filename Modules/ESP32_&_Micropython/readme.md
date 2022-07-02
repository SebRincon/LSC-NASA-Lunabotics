## ESP32 Microcontrolelr 
> The ESP32 can be programmed with the Arduino Environment or with MicroPython, in this project we chose MicroPython for all round simplicity.
___
## Programs 
### [hallSensorStepper.py]()
- This program will connect to a socket server and wait for message, then it will move forwards or backwards until the internal hall sensor is activated by a magnet, then it will stop.

### [relay_boot.py]()
- This program controls 4 seperate relays, with a activation and deactivation being done in pairs, we used this to make allow forwards and backwards movement on a DC motor.

### [motorControl.py]() 
- This program is the motor control base for the a4988 stepper motor controller.

### any other file with `boot` in the title
- These are boot programs that are ready to be loaded on to an ESP32.