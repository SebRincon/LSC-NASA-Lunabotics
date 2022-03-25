#! /usr/bin/env python3
from turtle import distance
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math
import time
# from turtlesim.msg import Pose
x = 0
y = 0

def move(velocity_publisher, speed, distance, is_forward):
    # declare a Twist message to send velocity commands
    velocity_message = Twist()
    # get current location
    # global x, y
    x0 = x  # save the initial location x-coordinate
    y0 = y  # save the initial location y-coordinate
    if (is_forward):
        velocity_message.linear.x = abs(speed)
    else:
        velocity_message. linear.x = -abs(speed)
    distance_moved = 0.0
    # we publish the velocity at 10 Hz (10 times a second)
    loop_rate = rospy.Rate(10)
    while True:
        rospy.loginfo("Turtlesim moves forwards")
        velocity_publisher.publish(velocity_message)
        loop_rate.sleep()
        # Pythagoras theorem
        distance_moved = abs(math.sqrt(((x-x0) ** 2) + ((y-y0) ** 2)))
        print(distance_moved)
        if not (distance_moved < distance):
            rospy.loginfo("reached")
            break
    # finally, stop the robot when the distance is moved
    velocity_message.linear.x = 0
    velocity_publisher.publish(velocity_message)


def poseCallback(pose_message):
    x = pose_message.pose.pose.position.x
    y = pose_message.pose.pose.position.y
    # yaw = pose_message.theta
    print(f"x:  {pose_message.pose.pose.position.x}")
    print(f"y:  {pose_message.pose.pose.position.y}")
    # print(type(pose_message))


if __name__ == '__main__':
    rospy.init_node('rover_control', anonymous=True)
    # declare velocity publisher
    cmd_vel_topic = '/cmd_demo'
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
    # _speed = input("Input Speed: ")
    # _distance = input("Distance Speed: ")
    _speed = 1
    _distance = 1
    position_topic = "/odom_demo"
    pose_subscriber = rospy.Subscriber(position_topic, Odometry, poseCallback)
    move(velocity_publisher, int(_speed), int(_distance), True)
    time.sleep(2)
