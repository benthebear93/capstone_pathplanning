#!/usr/bin/env python2

import cv2
import rospy
import numpy as np
import Img_process
import time
from sensor_msgs.msg import CompressedImage     ## use this to sub & pub the videodata
rospy.init_node('cam')

prevTime = 0
curTime = 0
def video_processing(ros_data):
    global prevTime, curTime
    curTime = time.time()
    np_arr = np.fromstring(ros_data.data, np.uint8)
    image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    frame = image_np
    '''img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(img_gray,(5,5),0)
    blur2 = cv2.GaussianBlur(frame,(5,5),0)
    #base_map = cv2.adaptiveThreshold(img_gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,15,2)
    lower = np.array([126, 134, 0])
    higher = np.array([255, 255, 255])
    lower2 = np.array([0,65,60])
    higher2 = np.array([40,152,255])
    g_l = np.array([59,61,0])
    g_h = np.array([100,255,255])
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    Gmask = cv2.inRange(hsv, lower, higher)
    Gmask2 = cv2.inRange(hsv,lower2,higher2)
    Gmask3 = cv2.inRange(hsv,g_l,g_h)'''
    #frame_thres=cv2.bitwise_and(base_map, Gmask)
    sec = curTime - prevTime
    prevTime = curTime
    fps = 1/(sec)
    print "Time {0} " , sec
    print "Estimated fps {0} " , fps
    str = "FPS : %0.1f" %fps
    cv2.putText(frame, str, (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
    #cv2.imshow('img_', Gmask3)
    #cv2.imshow('RED', Gmask)
    cv2.imshow('Yellow', frame)
    k = cv2.waitKey(1) & 0xFF


if __name__ == '__main__':
    sub = rospy.Subscriber('/usb_cam/image_raw/compressed', CompressedImage, video_processing)
    rospy.spin()
