#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from FRTF20blueliningmaxIV.srv import laser_service, action_service
# For testing the action service
from geometry_msgs.msg import Pose

# We need to establish directions, simple test drive forwards/left 
# and see how position of robot changes in laser coordinates
def init():
    print("SEEKING COORDINATE TRANSFORM")

    # Get position of robot from laser service.
    laserService = rospy.ServiceProxy('laser_service', laser_service)
    response = laserService()
    positionOld = response.position

    # Move forward in X axis 1 second
    msg = Twist()
    msg.linear.x = 1
    pub.publish(msg)
    rospy.sleep(1)
    msg.linear.x = 0
    pub.publish(msg)
    rospy.sleep(0.5)

    # Get new position from laser service
    response = laserService()
    positionNew = response.position

    # Derive the movement
    movement = positionNew.position.x - positionOld.position.x
    if movement > 0:
        signs[0] = 1
    else:
        signs[0] = -1

    # Get position of robot from laser service.
    response = laserService()
    positionOld = response.position

    # Move forward in X axis 1 second
    msg = Twist()
    msg.linear.y = 1
    msg.angular.z = 0.15
    pub.publish(msg)
    rospy.sleep(1)
    msg.linear.y = 0
    msg.angular.z = 0
    pub.publish(msg)
    rospy.sleep(0.5)

    # Get new position from laser service
    response = laserService()
    positionNew = response.position

    # Derive the movement
    movement = positionNew.position.z - positionOld.position.z
    if movement > 0:
        signs[1] = 1
    else:
        signs[1] = -1


rospy.init_node('main', anonymous=True)
rospy.wait_for_service('action_service')
rospy.wait_for_service('laser_service')

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

rate = rospy.Rate(10)

# Signs for forward/right
signs = [1, 1]

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
        msg.linear.x = signs[0] * 1
    elif action == "backward":
        msg.linear.x = signs[0] * -1
    elif action == "left":
        msg.linear.y = signs[1] * 1
        msg.angular.z = signs[1] * 0.15
    elif action == "right":
        msg.linear.y = signs[1] * -1 
        msg.angular.z = signs[1] * -0.15

    pub.publish(msg)
    rate.sleep()