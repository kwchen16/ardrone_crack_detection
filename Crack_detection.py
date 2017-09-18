#!/usr/bin/env python

# import the necessary packages
import rospy
from sensor_msgs.msg import Image, CameraInfo
import cv2, cv_bridge
from collections import deque
import numpy as np
import argparse


class Movement:
    def __init__(self):
        self.bridge = cv_bridge.CvBridge()
        #cv2.namedWindow("window",1)
        self.image_sub = rospy.Subscriber('ardrone/image_raw', Image, self.image_callback)
        ap = argparse.ArgumentParser()
        ap.add_argument("-v", "--video",
                        help="path to the (optional) video file")
        ap.add_argument("-b", "--buffer", type=int, default=32,
                        help="max buffer size")
        args = vars(ap.parse_args())

        self.pts = deque(maxlen=args["buffer"])

    def image_callback(self, msg):

        ap = argparse.ArgumentParser()
        ap.add_argument("-v", "--video",
                        help="path to the (optional) video file")
        ap.add_argument("-b", "--buffer", type=int, default=32,
                        help="max buffer size")
        args = vars(ap.parse_args())
        

	crackCascade = cv2.CascadeClassifier('cascade_2.xml')
        crackCascade1 = cv2.CascadeClassifier('cascade.xml')
	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = self.bridge.imgmsg_to_cv2(msg,desired_encoding= 'bgr8')
	
	cracks = crackCascade.detectMultiScale(frame,scaleFactor=1.1,minNeighbors=5,minSize=(100, 100),flags = 0)
        cracks1 = crackCascade1.detectMultiScale(frame,scaleFactor=1.1,minNeighbors=5,minSize=(100, 100),flags = 0)
	# Draw a rectangle around the faces
        if(len(cracks) == len(cracks1)):
		for (x, y, w, h) in cracks:
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

	
	# show the frame to our screen and increment the frame counter
	cv2.imshow("Frame", frame)
    
	key = cv2.waitKey(1) & 0xFF
	
rospy.init_node('movement')
movement = Movement()
rospy.spin()
