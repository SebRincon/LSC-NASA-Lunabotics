import time
import wpilib
import wpilib.drive
import logging


# from networktables import NetworkTables

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        pass
        # self.FrontLeftMotor = wpilib.Spark(1)
        # self.FrontRightMotor = wpilib.Spark(2)
        # self.BackLeftMotor = wpilib.Spark(3)
        # self.BackRightMotor = wpilib.Spark(4)

        # self.left = wpilib.SpeedControllerGroup(self.FrontLeftMotor, self.BackLeftMotor)
        # self.right = wpilib.SpeedControllerGroup(self.FrontRightMotor, self.BackRightMotor)

        # self.drive = wpilib.drive.DifferentialDrive(self.left, self.right)
        # self.timer = wpilib.Timer()
        # self.network = wpilib.SmartDashboard

        # self.network.putNumberArray('velocity',[0.5, 0.0])

    def disabledInit(self):
        self.FrontLeftMotor = wpilib.Spark(1)
        self.FrontRightMotor = wpilib.Spark(2)
        self.BackLeftMotor = wpilib.Spark(3)
        self.BackRightMotor = wpilib.Spark(4)

        self.left = wpilib.SpeedControllerGroup(self.FrontLeftMotor, self.BackLeftMotor)
        self.right = wpilib.SpeedControllerGroup(self.FrontRightMotor, self.BackRightMotor)

        self.drive = wpilib.drive.DifferentialDrive(self.left, self.right)
        self.timer = wpilib.Timer()
        self.network = wpilib.SmartDashboard

        self.network.putNumberArray('velocity',[0.5, 0.5])

    def disabledPeriodic(self):
    
        """This function is called periodically during autonomous."""

        _velocity = self.network.getNumberArray(key='velocity', defaultValue=[0.5,0.5])
        # print(_velocity)
        self.drive.arcadeDrive(_velocity[0], _velocity[1])  # Drive forwards at half speed

if __name__ == '__main__':
    wpilib.run(MyRobot)