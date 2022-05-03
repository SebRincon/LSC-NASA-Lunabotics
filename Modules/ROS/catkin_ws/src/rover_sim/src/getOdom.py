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

def poseCallback(pose_message):
    x = pose_message.pose.pose.position.x
    y = pose_message.pose.pose.position.y
    # yaw = pose_message.theta
    print(f"x:  {pose_message.pose.pose.position.x}")
    print(f"y:  {pose_message.pose.pose.position.y}")
    # print(type(pose_message))


if __name__ == '__main__':
    rospy.init_node('rover_sim_pose', anonymous=True)

    # declare velocity publisher

    position_topic = "/odom_demo"
    pose_subscriber = rospy.Subscriber(position_topic, Odometry, poseCallback)

    time.sleep(2)
