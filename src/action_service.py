#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Pose
from FRTF20blueliningmaxIV.srv import action_serviceResponse, action_service

def callback(msg):
    response = action_serviceResponse()

    distances = msg.distanceToGo

    x = distances.position.x
    z = distances.position.z

    # Denna gräns måste ändras så att 3d printer kommer tillräckligt nära för att göra blueline
    # Värdet kommer vara i samma mått som laser förmodligen mm
    if (x**2 + z**2)**0.5 < 40: # Distance small enough for 3d printer to make the dot
       response.action = "stop"
    elif abs(x) > abs(z): # We move in the largest error
        if x > 0:
            response.action = "forward"
        else:
            response.action = "backward"
    else:
        if z > 0:
            response.action = "left"
        else:
            response.action = "right"

    return response

rospy.init_node('action_service', anonymous=True)
srv = rospy.Service('action_service', action_service, callback)

rospy.spin()