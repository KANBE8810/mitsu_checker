#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import rospy
import cv2
import numpy as np
from std_msgs.msg import Int32
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class image_converter:
    def __init__(self):
        self.image_pub = rospy.Publisher("image_topic", Image, queue_size=1)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/usb_cam/image_raw",Image,self.callback)

    def callback(self,data):
        pub1 = rospy.Publisher("face_x", Int32, queue_size=1)
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')

        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        face = faceCascade.detectMultiScale(gray,1.1,3,minSize=(50,50))
        for (x,y,w,h) in face:
            xx = x+w
            yy = y +h
            print(xx/2, yy/2)
            pub1.publish(xx)
#        print(face)

        for (x,y,w,h) in face:
            cv2.rectangle(gray,(x,y),(x+w,y+h),(255,0,255),thickness=5)
            cv2.imshow("frame_orig",gray)
            cv2.waitKey(3)
#        cv2.imshow('detected_face', cv_image)
#        cv2.waitKey(3)

def main(args):
    rospy.init_node('image_converter', anonymous=True)
    ic = image_converter()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
    rospy.spin()
