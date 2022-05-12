# 2022 Cyfair Lunabotics


## Rover Control & Automation


#### [CONTROL METHOD]() 
We have gone with partial automation & manual control of the locomotion, excavation and deposition systems, but we have implemented an automated system to interchange between modes.

#### [AUTOMATED  CONTROL HARDWARE]() 
We are using ROS to handle a LIDAR & RGBD camera, ROS is running on the raspberry pi where it takes in the data from the sensors and passes it to be processed by a  SLAM algorithm where the Velocity and Angular data is which is relayed to the RoboRIO.

#### [MANUAL  CONTROL HARDWARE]() 
We are using the Raspberry Pi 4 as the access point for our wiress control, the data is from a gamepad connected to a PC where the data is processed  and Velocity and Direction Units are then sent to the RoboRIO via the NetworkTables protocol on the RoboRIO which then allows the RoboRIO to control the  motors.

#### [AUTOMATED GEARBOX]() 
As for our automated mode switching, we are using ESP32 Microcontrollers to handle the gearbox motors and sensors. The program that is running on the ESP32’s connects the Raspberry Pi wirelessly with a TCP socket connection. On command the ESP32 will detect where the gearbox is engaged and move to engage the other subsystem.
Final Configuration

#### [FINAL CONFIG ON THE CC SIDE]() 
The Final configuration would be manual control from a gamepad attached to a PC which sends data wirelessly to a Raspberry PI, then the PI relays the data to the RoboRIO which has control over the motors.
                                                                         
                                                                         
                                                        
                                                                         
                                                                         
                                                                         
       ┌─Driver Station────┐                         ┌ ROVER ───────────┐
       │               ┌───┴─────────┐        TCP    │    ┌─────────┐   │
       │               │ Controller  │◀─────Socket───┼───▶│  RPI4   │   │
       │               └───┬─────────┘      │        │    └────▲────┘   │
       │               ┌───┴──┐             │        │         ┃        │
       │               │ GUI  │◀────────────┘        │         ┃        │
       │               └───┬──┘                      │         ┃        │
       └───────────────────┘                         │   NetworkTables  │
                                                     │         ┃        │
                                                     │         ┃        │
                                                     │         ┃        │
                                                     │ ┌───────▼───────┐│
                                                     │ │    RoboRIO    ││
                                                     │ └───────────────┘│
                                                     │         │        │
                                                     │         │        │
                                                     │         ▼        │
                                                     │ ┌───────────────┐│
                                                     │ │    Motors     ││
                                                     │ └───────────────┘│
                                                     └──────────────────┘
                                                     
                                                     

### Hardware

## [ROS](https://www.github.com)
ROS is being used as the main automation control point, using an `RPLidar A1` paired with the `HECTOR-SLAM` algorithm for localization and path planning.

## [RoboRIO]()
The RoboRIO is being used as main controller board, where most motors will be connected to and paired with the `WPILib` Java library we are able to control the motors very precisely. 
## [Raspberry PI]()
We are using the `Raspberry PI 4 8GB` as a wireless communication and control point as well as the main processors for any sensors. We are using ROS to handle the sensors and handle the path planning. We are also running a TCP server on the PI to path data to and from the driver station.

## [ESP32]()
We are using the ESP32 microcontroller board running microPython as the motor controllers for the `Nema Stepper Motors` as they are not controllable with the RoboRIO and they also handle the `Hall sensors` inputs for the gearbox poistions. They are running a TCP client that connects to the PI which allows for wireless control of the stepper motors from the PI.

## Protocols & Special Applications
- [TCP Socket]()
- [Network Tables]()
- [microPython]()
- [ROS]()
- [SLAM]()
- [DepthAI]()
