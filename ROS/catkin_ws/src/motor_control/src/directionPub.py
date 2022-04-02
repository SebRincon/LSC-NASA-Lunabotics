#!/usr/bin/env python3

import rospy
import threading
from std_msgs.msg import String
from networktables import NetworkTables

class MotorControl():
    def setup(self):
        _stopSpeed=0
        _stopAngle=0

        self.cond = threading.Condition()
        self.notified = [False]
        
        # NetworkTables.initialize(server='10.xx.xx.2')
        NetworkTables.initialize(server='127.0.0.1')
        NetworkTables.addConnectionListener(self.connectionListener, immediateNotify=True)

        with self.cond:
            print("Waiting")
            if not self.notified[0]:
                self.cond.wait()

        self.motorTable = NetworkTables.getTable('SmartDashboard')
        self.motorTable.putNumberArray('velocity',[_stopSpeed, _stopAngle])
        _motorFeedback = self.motorTable.getNumberArray(key='MotorFeedback', defaultValue=[2.0,2.0])
        if _motorFeedback == [_stopSpeed, _stopAngle]:
            print("Motors Okay")
        else:
            print("Network Table issue")

    def connectionListener(self, connected, info):
        print(info, '; Connected=%s' % connected)
        with self.cond:
            self.notified[0] = True
            self.cond.notify()


    def setVelocity(self, speed:float, angle:float):
        self.motorTable.putNumberArray('velocity',[speed, angle])

    def velocityCallback(self, message:String):
        ## Assuming the message is in format '0.00.0' for testing 
        _xSpeed = float(message.data[:3])
        _zRotation = float(message.data[3:])
        self.setVelocity(_xSpeed, _zRotation)


def listener():
    motors = MotorControl()
    motors.setup()
    
    # Create node and set unique id 
    rospy.init_node('motor_control', anonymous=True)

    # Subscribe to the topic - data type - callback
    rospy.Subscriber('motor_control/direction', String, motors.velocityCallback)

    # start listening in a loop
    rospy.spin()


if __name__ == '__main__':
    listener()
