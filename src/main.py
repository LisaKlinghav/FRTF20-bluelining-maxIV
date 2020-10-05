#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

rospy.init_node('main', anonymous=True)
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

msg = Twist()
msg.linear.x = 0
rate = rospy.Rate(10)

while not rospy.is_shutdown():
    pub.publish(msg)
    rate.sleep()