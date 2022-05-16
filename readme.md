# 2022 Cyfair Lunabotics

## Rover Control & Automation

#### [CONTROL METHOD]()

We have gone with partial automation & manual control of the locomotion, excavation and deposition systems, but we have implemented an automated system to interchange between modes.

#### [AUTOMATED CONTROL HARDWARE]()

We are using ROS to handle a LIDAR & RGBD camera, ROS is running on the raspberry pi where it takes in the data from the sensors and passes it to be processed by a SLAM algorithm where the Velocity and Angular data is which is relayed to the RoboRIO.

#### [MANUAL CONTROL HARDWARE]()

We are using the Raspberry Pi 4 as the access point for our wiress control, the data is from a gamepad connected to a PC where the data is processed and Velocity and Direction Units are then sent to the RoboRIO via the NetworkTables protocol on the RoboRIO which then allows the RoboRIO to control the motors.

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

# FRC-ROS

This is the source code for using ROS with an FRC Robot. The steps for installing and running ROS applications are identical for desktop PC's, laptops, Raspberry PI, NVidia Jetson.

## Youtube Demos

Simulation Demo: https://www.youtube.com/watch?v=qSjgmY7hYsY

Teleop Demo w/ SLAM: https://www.youtube.com/watch?v=1Qe-s1liH5k

Autonomous and Swerve Simulation: https://youtu.be/OrnWRP20IEY

## Setup

Setup is fairly simple. You will need a computer with Ubuntu 16.04 installed.

### 1. Install Ubuntu on Your Computer

Make sure you have Ubuntu 20.04 installed on your computer: https://tutorials.ubuntu.com/tutorial/tutorial-install-ubuntu-desktop-1604#0

### 2. Download FRC-ROS to Your Computer

Enter the following to download FRC-ROS to your Documents:

```
git clone https://github.com/SebRincon/LSC-NASA-Lunabotics.git
```

### 3. Make Updates When Needed

If you make changes to the source code, you will need to update the files from the location where you downloaded FRC-ROS to your Catkin workspace. Open a terminal and put the following command to bring up the simulation:

```
cd ~/Documents/FRC-ROS
```

### ~~ Run a Simulation ~~ (to-do/fix)

You can run a robot simulation in Gazebo simulator. Open a terminal and put the following command to bring up the simulation:

```
roslaunch (package_here) (launch_here)
```

The options include the following and can be typed in similar to above:

- [] auton: Enables autonomous nagivation and driving.
- [] kinectlidar: Starts up a Kinect and RPLidarA2 connected over USB.
- [] robot: FOR THE REAL ROBOT. This brings up all sensors and the bridge to the roboRIO.
- [] sim: Brings up a simulation.
- [] slam: Enables SLAM (Simeltaneous Localization and Mapping)
- [] teleop: Enables teleop control through either GUI or any joystick such as an XBox controller.
- [] user_interface: Brings up GUI for viewing and sending data to ROS.
- [] visualize: Bring up RViz used to visualize ROS data.

## To-Do

### Implement a Network Tables Interface for RoboRIO

This requires 2 parts. The first part is a ROS package capable of communicating over FRC Network Tables. The second part needs a software interface on the RoboRIO to send and receive data to and from the Jetson.

Interface will be like this:

RoboRio Software (RoboRio) <--Network Tables--> ROS Converter Node (Rasp) <-- ROS Topics --> ROS Software (Rasp)

### Implement Commands and Data Transfer

The following data is the most essential data that will be transferred:

- Velocity Commands (Rasp -> RoboRIO) (required)
- Send IMU measurements (RoboRIO -> Rasp) (optional)
- Send Wheel Odometry (RoboRIO -> Rasp) (optional)

The folowing data will allow for usability in competition:

- Send Commands (RoboRIO -> Rasp)
- Receive Status (Rasp -> RoboRIO)

Commands from RoboRIO -> Rasp could include stuff like:

- Set navigation goals.
- Activate target tracking.
- Switch to Mapping-Mode (SLAM) or Localization-Only (needs existing map)

Status from Rasp -> RoboRIO could include stuff like:

- Target tracking info
- Localization info
- Navigation statuses
- General ROS Status

Related Resources:

- https://www.chiefdelphi.com/t/controlling-a-roborio-through-a-raspberry-pi-a-wifi-router/392841
- https://willhaley.com/blog/raspberry-pi-wifi-ethernet-bridge/
- [Network Diagram Example](https://imgur.com/a/D1wnLnD)

### Implement Target Tracking

A single ROS node can take any camera data and perform image processing. This can be written and configured however the user likes and can output targeting data. A single node can be run, or multiple nodes can be doing processing on the same camera feed.

## Tutorials and Helpful Information

### Recommended Tutorials to Get Started

Getting Started:

- http://wiki.ros.org/
- http://wiki.ros.org/ROS/Tutorials

Additional Tutorials:

- http://wiki.ros.org/urdf/Tutorials
- http://gazebosim.org/tutorials?tut=ros_overview
- http://wiki.ros.org/rviz/Tutorials
- http://wiki.ros.org/navigation/Tutorials

### Packages and Software Used in FRC-ROS

Some sensor packages are included here:

- http://wiki.ros.org/rplidar
- http://wiki.ros.org/openni_launch

SLAM (Simeltaneous Localization and Mapping):

- https://en.wikipedia.org/wiki/Simultaneous_localization_and_mapping
- http://wiki.ros.org/hector_mapping
- http://wiki.ros.org/gmapping
- http://wiki.ros.org/rtabmap_ros

Robot Localization:

- https://roscon.ros.org/2015/presentations/robot_localization.pdf
- http://docs.ros.org/kinetic/api/robot_localization/html/index.html
- http://www.cs.cmu.edu/~rasc/Download/AMRobots5.pdf

Autonomous Navigation:

- https://en.wikipedia.org/wiki/Robot_navigation
- http://wiki.ros.org/move_base
- http://wiki.ros.org/costmap_2d
- http://wiki.ros.org/nav_core
- http://wiki.ros.org/navfn
- http://wiki.ros.org/dwa_local_planner

### Other Relevant Topics

Swerve Drive Kinematics:

- https://www.chiefdelphi.com/t/paper-4-wheel-independent-drive-independent-steering-swerve/107383

Machine learning is a more advanced topic:

- https://www.youtube.com/watch?v=aircAruvnKk
- https://developer.nvidia.com/embedded/twodaystoademo
- https://github.com/dusty-nv/ros_deep_learning
