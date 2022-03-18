from threading import current_thread
import rospy
from std_msgs.msg import String
import RPi.GPIO as io

global direction
direction = 0 


class MotorControl():
    def setup(self):
        io.setmode(io.BOARD)
        io.setup(12,io.OUT)
        io.setup(33,io.OUT)
        io.setup(32,io.OUT)
        io.setup(35,io.OUT)

        self.frontRightMotor = io.PWM(12,100)
        self.fronLeftMotor = io.PWM(33,100)
        self.backRightMotor = io.PWM(32,100)
        self.backLeftMotor = io.PWM(35,100)

        self.direction = 50

        self.frontRightMotor.start(self.direction)
        self.fronLeftMotor.start(self.direction)
        self.backRightMotor.start(self.direction)
        self.backLeftMotor.start(self.direction)


        stop = False

    def setVelocity(self,dutycycle):
        print(dutycycle)
        self.direction = dutycycle

        self.frontRightMotor.ChangeDutyCycle(int(self.direction))
        self.fronLeftMotor.ChangeDutyCycle(int(self.direction))
        self.backRightMotor.ChangeDutyCycle(int(self.direction))
        self.backLeftMotor.ChangeDutyCycle(int(self.direction))

    def setDirection(self, genDirection):
        genDirection = genDirection.data
        directions = {
                'f': [4,24,4,24],
                'b': [24, 4, 24, 4],
                's': [0,0,0,0],
                'fl': [0,0,0,0],
                'fr': [0,0,0,0],
                'br': [0,0,0,0],
                'bl': [0,0,0,0],
                'r': [0,0,0,0],
                'l': [0,0,0,0],
                }


        self.frontRightMotor.ChangeDutyCycle(directions[genDirection][0])
        self.fronLeftMotor.ChangeDutyCycle(directions[genDirection][1])
        self.backRightMotor.ChangeDutyCycle(directions[genDirection][2])
        self.backLeftMotor.ChangeDutyCycle(directions[genDirection][3])


    def set_speed_w_directions(self, message):
        # Message should be in json format
        # {
        # speed: int,
        # distance: int,
        # direction: string 
        # }
        
        _message = message.data
        speed = int(_message['speed'])
        current_distance = 0.0
        t0 = rospy.Time.now().to_sec()

        # Tracking distance traveled with a linear equation distance = speed * time
        while current_distance < int(_message['distance']):
            self.setDirection(_message['direction'])
            t1 = rospy.Time.now().to_sec()
            current_distance = speed * (t1-t0)
            



def listener():
    motors = MotorControl()
    motors.setup()
    
    # Create node and set unique id 
    rospy.init_node('motor_control', anonymous=True)
    # Subscribe to the topic - data type - callback
    rospy.Subscriber('motor_control/direction', String, motors.setDirection)
    # start listening in a loop
    rospy.spin()


if __name__ == '__main__':
    listener()
