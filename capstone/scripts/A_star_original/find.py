#!/usr/bin/env python2

import cv2
import rospy
import numpy as np
import Img_process
from resize import resize
from astar import astar
from sensor_msgs.msg import CompressedImage     ## use this to sub & pub the videodata
from capstone_msgs.msg import Smartfactory

rospy.init_node('cam')
pub = rospy.Publisher('/mobilepath_list', pathlist, queue_size=100)

flag = 0

def sendPath(path_list):
	print(path_list)
	pub.publish(path_list)

def finding_path(ros_data):

    global flag
    np_arr = np.fromstring(ros_data.data, np.uint8)
    image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    frame = image_np
    start_point = Img_process.Basic_map()
    end_point = Img_process.Basic_map()
    obstacle_map = Img_process.Basic_map()

    ret_start,start_x, start_y, start_img, s_w, s_h = start_point.find(frame, 'RED')
    ret_end, end_x, end_y, end_img, e_w, e_h = end_point.find(frame, 'BLUE')
    print (ret_start, ret_end)
    capstone_map = obstacle_map.obstacle_load(frame)

    if ret_start == 1 and ret_end == 1:
        start = (int(start_x), int(start_y))
        end = (int(end_x), int(end_y))
        print("start:", start)
        print("end", end)
        if flag == 0:
            path = astar(capstone_map, start, end)
            print (path)
    else:
        print(" no image, setting random start,end poinst ")
        #start = (10,10)
        #end = (330, 330)
    #re_start = (int(start[0]/4), int(start[1]/4))
    #re_end = (int(end[0]/4), int(end[1]/4))

    #obstacle_resize = resize(capstone_map)
    #print("going in astar function? ")
    #path2  = astar(obstacle_resize, re_start, re_end)

    #cv2.circle(obstacle_resize, re_start, 3, (0, 0, 255), 3)

    if path is not None and flag == 0:
        print ("here? path circle ")
        if len(path)>0:
            for i in range(0, len(path)):
                print("path:", path[i])
                cv2.circle(frame, path[i], 1, (0,0,255), 1)
                # cv2.imwrite('/home/benlee/catkin_ws/src/find_path/script/path.png',frame, params=[cv2.IMWRITE_PNG_COMPRESSION,0])
                # cv2.imwrite('/home/benlee/catkin_ws/src/find_path/script/cap.png',capstone_map, params=[cv2.IMWRITE_PNG_COMPRESSION,0])
                cv2.imwrite('catkin_ws/src/capstone_vision/scripts/path.png',frame, params=[cv2.IMWRITE_PNG_COMPRESSION,0])
                cv2.imwrite('catkin_ws/src/capstone_vision/scripts/cap.png',capstone_map, params=[cv2.IMWRITE_PNG_COMPRESSION,0])
                flag = 1
    else:
        print("no path bro")

    cv2.imshow('img', frame)
    cv2.imshow('start_img', start_img)
    cv2.imshow('end_img', end_img)
    cv2.imshow('obstacle', capstone_map)
    #cv2.imshow('resized map',obstacle_resize)
    cv2.waitKey(1) & 0xFF

if __name__ == '__main__':

    sub = rospy.Subscriber('/usb_cam/image_raw/compressed', CompressedImage, finding_path)
    sub = rospy.Subscriber('/usb_cam/image_raw/', CompressedImage, finding)
    rospy.spin()
