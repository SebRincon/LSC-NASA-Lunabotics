# 2022 Cyfair Lunabotics

                                                                         
                                                                         
                                                        
                                                                         
                                                                         
                                                                         
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
