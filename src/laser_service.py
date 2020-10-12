#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Pose
from nav_msgs.msg import Odometry
from FRTF20blueliningmaxIV.srv import laser_serviceResponse, laser_service

def callback(msg):
    response = laser_serviceResponse()
    # For testing purposes, later we want the laser data instead
    # Gets the robot location in the enviroment
    robotOdom = rospy.wait_for_message('/odom', Odometry)

    # TODO: Get laserdata to determin distances to go
    response.distanceToGo = robotOdom.pose.pose

    response.success = True
    return response

rospy.init_node('laser_service', anonymous=True)
srv = rospy.Service('laser_service', laser_service, callback)

rospy.spin()