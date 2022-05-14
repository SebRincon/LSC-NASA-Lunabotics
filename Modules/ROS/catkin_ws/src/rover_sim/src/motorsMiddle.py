#! /usr/bin/env python3
import rospy
import socket
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import threading
from networktables import NetworkTables



class motorsMiddle():

    def setup(self):
        # irellivant 
        self.cond = threading.Condition()
        self.notified = [False]
        
        # NetworkTables.initialize(server='10.xx.xx.2')
        NetworkTables.initialize(server='169.254.69.69')
        NetworkTables.addConnectionListener(self.connectionListener, immediateNotify=True)
        self.smart_dashboard = NetworkTables.getTable('SmartDashboard')
        self.datatable = NetworkTables.getTable('datatable')

        # wait for connection 
        with self.cond:
            print("Waiting")
            if not self.notified[0]:
                self.cond.wait()

        # Get table from networktables
        self.motorTable = NetworkTables.getTable('SmartDashboard')

        # Set Default value for testing
        self.motorTable.putNumberArray('velocity',[0,0])
        # Grab values from network table for testing
        _motorFeedback = self.motorTable.getNumberArray(key='velocity', defaultValue=[2.0,2.0])

        # Test Connection
        if _motorFeedback == [0,0]:
            print("Motors Okay")
        else:
            print("Network Table issue")


    def sendControl(self, message):
        self.datatable.putNumber('RightStickValue', message.linear)
        self.datatable.putNumber('LeftStickValue',  message.angular)

    def listener(self):
        rospy.init_node('listener', anonymous=True)
        rospy.Subscriber('teleop', Twist, self.sendControl)


if __name__ == "__main__":

    motorsControl = motorsMiddle()
    motorsControl.setup()
    motorsControl.listener()