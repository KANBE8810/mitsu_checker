#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame.mixer
import time
import rospy
from std_msgs.msg import Int32
import message_filters

def callback(mgs1,mgs2):
#   print(mgs1.data)
#   print(mgs2.data)
    if mgs1.data == 1:
       pygame.mixer.music.load('m.mp3')
       pygame.mixer.music.play(1)
       time.sleep(1)
    elif mgs2.data > 2:
       pygame.mixer.music.load('m.mp3')
       pygame.mixer.music.play(1)
       time.sleep(2)

def main():
    pygame.mixer.init()
    print("密チェッカー起動中")
    rospy.init_node("mitsu_node")
    sub1 = message_filters.Subscriber("distance_to_PC",Int32)
    sub2 = message_filters.Subscriber("number_of_poeple",Int32)
    queue_size = 10
    fps = 100.
    delay = 1 / fps * 0.5

    mf = message_filters.ApproximateTimeSynchronizer([sub1, sub2], queue_size, delay,allow_headerless=True )
    mf.registerCallback(callback)
    rospy.spin()

if __name__ == "__main__":
    try:
        if not rospy.is_shutdown():
            main()
    except rospy.ROSInterruptException:
        pass
