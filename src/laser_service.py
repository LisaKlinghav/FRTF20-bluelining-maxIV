#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Pose
from nav_msgs.msg import Odometry
from FRTF20blueliningmaxIV.srv import laser_serviceResponse, laser_service
import socket

class UDP_connect:
    def __init__(self, ip, port, buffersize):
        self._ip = ip
        self._port = port
        self._buffersize = buffersize

        self._UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self._UDPServerSocket.bind((self._ip, self._port))
        self._UDPServerSocket.settimeout(5)

    def get_message(self):
        try:
            bytesAddressPair = self._UDPServerSocket.recvfrom(self._buffersize)
        except socket.timeout:
            return False 
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]

        return [message, address]

def callback(msg):
    response = laser_serviceResponse()
    response.success = True

    distancesMessage = distancesUDP.get_message()
    positionMessage = positionUDP.get_message()
    if not distancesMessage or not positionMessage:
        response.success = False
        
    else:
        # X,9.6879549857494169e+002,Y,-2.1040698523077076e+003,Z,-6.7986554237869018e+002 example line from laser
        distancesSplit = distancesMessage[0].split(",")
        distanceX = float(distancesSplit[1])
        distanceZ = float(distancesSplit[5])

        distances = Pose()
        distances.position.x = distanceX
        distances.position.z = distanceZ

        positionSplit = positionMessage[0].split(",")
        positionX = float(positionSplit[1])
        positionZ = float(positionSplit[5])

        position = Pose()
        position.position.x = positionX
        position.position.z = positionZ

        response.distanceToGo = distances
        response.position = position

    return response

rospy.init_node('laser_service', anonymous=True)
srv = rospy.Service('laser_service', laser_service, callback)

localIP     = "192.168.79.75"
localPortDistances = 65432
localPortPosition = 65433
bufferSize  = 1024

distancesUDP = UDP_connect(localIP, localPortDistances, bufferSize)
positionUDP = UDP_connect(localIP, localPortPosition, bufferSize)

rospy.spin()