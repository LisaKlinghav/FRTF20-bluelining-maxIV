#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from FRTF20blueliningmaxIV.srv import laser_service, action_service
# For testing the action service
from geometry_msgs.msg import Pose

rospy.init_node('main', anonymous=True)
rospy.wait_for_service('action_service')
rospy.wait_for_service('laser_service')

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

rate = rospy.Rate(10)

# For testing our action server
xs = [1000, 500, 300, 200, -100, 0]
zs = [700, 700, 400, 100, -50, 0]
index = 0
time = 0

while not rospy.is_shutdown():
    msg = Twist() # Message to move the robot

    # laserReq = laser_serviceRequest()
    # distances = rospy.ServiceProxy('laser_service', laserReq)

    actionService = rospy.ServiceProxy('action_service', action_service)
    actionReq = Pose()
    actionReq.position.x = xs[index]
    actionReq.position.z = zs[index]
    action = actionService(actionReq)

    time += 1

    if index < 5 and time % 1000 == 0:
        index += 1

    action = action.action

    if action == "forward":
        msg.linear.x = 1
    elif action == "backward":
        msg.linear.x = -1
    elif action == "left":
        msg.linear.y = 1
        msg.angular.z = 0.15
    elif action == "right":
        msg.linear.y = -1 
        msg.angular.z = -0.15

    pub.publish(msg)
    rate.sleep()