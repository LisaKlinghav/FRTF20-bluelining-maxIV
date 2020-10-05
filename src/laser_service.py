#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Pose
from nav_msgs.msg import Odometry
from FRTF20blueliningmaxIV.srv import laser_serviceResponse, laser_service

def callback(msg):
    # TODO: Get laserdata to determin our location
    robotCurr = robotOdom.pose.pose
    if msg.find:
        robotNext = robotOdom.pose.pose
        robotNext.position.x += 1

    response = laser_serviceResponse()
    response.success = True
    return response

rospy.init_node('laser_service', anonymous=True)
srv = rospy.Service('laser_service', laser_service, callback)

# For testing purposes, later we want the laser data instead
# Gets the robot location in the enviroment
robotOdom = Odometry()
def positionCallback(msg):
    robotOdom = msg

robot_odom = rospy.Subscriber('/odom', Odometry, positionCallback)

r = rospy.Rate(10) # 10hz
while not rospy.is_shutdown():
    currPos.publish(robotCurr)
    nextPos.publish(robotNext)
    r.sleep()