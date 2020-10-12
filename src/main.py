#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from FRTF20blueliningmaxIV.srv import laser_serviceRequest, action_serviceRequest
# For testing the action service
from geometry_msgs.msg import Pose

rospy.init_node('main', anonymous=True)
rospy.wait_for_service('action_service')
rospy.wait_for_service('laser_service')

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

rate = rospy.Rate(10)

# For testing our action server
class ActionTest:
    def __init__(self):
        rospy.Subscriber("action", Pose, self.callback)
        self.distances = Pose()

    def callback(self, msg):
        self.distances = msg

    def get_distances(self):
        return self.distances
    
actionTest = ActionTest()

while not rospy.is_shutdown():
    msg = Twist() # Message to move the robot

    # laserReq = laser_serviceRequest()
    # distances = rospy.ServiceProxy('laser_service', laserReq)


    actionReq = action_serviceRequest()
    actionReq.distanceToGo = actionReq.get_distances()

    actionResp = rospy.ServiceProxy('action_service', actionReq)
    action = actionResp.action

    if action == "forward":
        msg.linear.x = 1
    elif action == "backward":
        msg.linear.x = -1
    elif action == "left":
        msg.linear.y = 1
        msg.angular.z = 0.2
    elif action == "right":
        msg.linear.y = -1 
        msg.angular.z = -0.2

    pub.publish(msg)
    rate.sleep()