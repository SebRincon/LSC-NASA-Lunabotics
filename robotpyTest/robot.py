import time
import wpilib
import logging
from networktables import NetworkTables

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        self.FrontLeftMotor = wpilib.Spark(1)
        self.FrontRightMotor = wpilib.Spark(2)
        self.BackLeftMotor = wpilib.Spark(3)
        self.BackRightMotor = wpilib.Spark(4)

        self.left = wpilib.SpeedControllerGroup(self.FrontLeftMotor, self.BackLeftMotor)
        self.right = wpilib.SpeedControllerGroup(self.FrontRightMotor, self.BackRightMotor)

        self.drive = wpilib.drive.DifferentialDrive(self.left, self.right)
        self.timer = wpilib.Timer()

        self.NetworkTables.initialize()
        self.sd = NetworkTables.getTable("SmartDashboard")

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.timer.reset()
        self.timer.start()

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""

        # Drive for two seconds
        if self.timer.get() < 2.0:
            self.drive.arcadeDrive(-0.5, 0)  # Drive forwards at half speed
        else:
            self.drive.arcadeDrive(0, 0)  # Stop robot

if __name__ == '__main__':
    wpilib.run(MyRobot)