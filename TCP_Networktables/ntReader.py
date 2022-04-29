#!/usr/bin/env python3

import threading
from networktables import NetworkTables
from time import sleep

class MotorControl():
    def setup(self):


        self.cond = threading.Condition()
        self.notified = [False]
        
        # NetworkTables.initialize(server='10.xx.xx.2')
        NetworkTables.initialize(server='169.254.69.69')
        NetworkTables.addConnectionListener(self.connectionListener, immediateNotify=True)
        self.smart_dashboard = NetworkTables.getTable('SmartDashboard')

        with self.cond:
            print("Waiting")
            if not self.notified[0]:
                self.cond.wait()

        self.motorTable = NetworkTables.getTable('SmartDashboard')
        self.motorTable.putNumberArray('velocity',[0,0])
        _motorFeedback = self.motorTable.getNumberArray(key='velocity', defaultValue=[2.0,2.0])
        if _motorFeedback == [0,0]:
            print("Motors Okay")
        else:
            print("Network Table issue")

        while True:
            print(f"Network table reades: {self.motorTable.getString('data', 'null')}")
            # sleep(0)

    def connectionListener(self, connected, info):
        print(info, '; Connected=%s' % connected)
        with self.cond:
            self.notified[0] = True
            self.cond.notify()


def listener():
    motors = MotorControl()
    motors.setup()
    motors.startSocketServer()
    # motors.startInput()


if __name__ == '__main__':
    listener()
