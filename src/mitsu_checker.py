#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import rospy
import cv2
import numpy as np
from std_msgs.msg import Int32
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class mitsu_checker:
    def __init__(self):
        self.image_pub = rospy.Publisher("image_topic", Image, queue_size=1)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/usb_cam/image_raw",Image,self.callback)

    def callback(self,data):
        flag1=0
        flag2=0
        pub1 = rospy.Publisher("distance_to_PC", Int32, queue_size=1)
        pub2 = rospy.Publisher("number_of_poeple", Int32, queue_size=1)
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')

#        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        face = faceCascade.detectMultiScale(cv_image,1.1,3,minSize=(50,50))
#            pub1.publish(xx/2)
#            pub2.publish(yy/2)

        if len(face) > 0:
            for rect in face:
                cv2.rectangle(cv_image, tuple(rect[0:2]), tuple(rect[0:2]+rect[2:4]), (255, 255, 255), thickness=2)
                if rect[2] >250:
                    flag1 = 1
            if len(face) > 2:
                flag2 = len(face)

        pub1.publish(flag1)
        pub2.publish(flag2)

        if flag1 != 0 or flag2 != 0:
            img2 = cv2.imread('mitsu.png')
            nimg2 =cv2.resize(img2,(100,100))
            x_offset=0
            y_offset=0
#            large_img = cv_image
#            small_img = nsrc
#            large_img[y_offset:y_offset+small_img.shape[0], x_offset:x_offset+small_img.shape[1]] = small_img
            cv_image[y_offset:y_offset+nimg2.shape[0], x_offset:x_offset+nimg2.shape[1]] = nimg2
            cv2.putText(cv_image,'warning',(100,300), cv2.FONT_HERSHEY_SIMPLEX, 3,(0,0,255),2,)
#        cv2.imshow('mitsu_checker',cv_image)
        cv2.imshow('mitsu_checker',cv_image)
        cv2.waitKey(3)

def main(args):
    rospy.init_node('mitsu_checker', anonymous=True)
    ic = mitsu_checker()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
    rospy.spin()
