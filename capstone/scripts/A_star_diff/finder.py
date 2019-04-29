#!/usr/bin/env python2
import cv2
import rospy
import numpy as np
import Img_process_gird
import matplotlib.pyplot as plt
from pathsolver import solver

from sensor_msgs.msg import CompressedImage     ## use this to sub & pub the videodata
from std_msgs.msg import Int32MultiArray
from capstone_msgs.msg import *


rospy.init_node('camera_nodes')
pub = rospy.Publisher("/point_lists", Int32MultiArray ,queue_size = 1)

final_path = 0
flag = 0

def line(route):
    xc=[]
    yc=[]
    for i in (range(0,len(route))):
        x=route[i][0]
        y=route[i][1]
        xc.append(x)
        yc.append(y)
    return xc,yc

def finding_path(ros_data):
    global flag, final_path, route_draw, captured

    ## Decodes the frame
    # image_np = Img_process_grid.capture(ros_data)
    np_arr = np.fromstring(ros_data.data, np.uint8)
    image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    ## Class Declaration
    Base_map = Img_process_gird.Basic_map()
    start_point = Img_process_gird.Basic_map()
    end_point = Img_process_gird.Basic_map()

    ### find mobile, end point and obstacle by using image_processing (HSV)
    ret_start,start_x, start_y, s_w, s_h ,start_img_= start_point.find(image_np, 'YELLOW')
    ret_end, end_x, end_y, e_w, e_h, end_img_ = end_point.find(image_np, 'RED')
    obstacle_img = Base_map.Gmask_for_start_end(image_np, 'GREEN') #obstacle binary image

    obj = Img_process_gird.gridmaker(20, obstacle_img)
    grid = obj.returnGrid()
    solve = solver()

    # print ('ret_start, ret_end : ', ret_start, ret_end)  ### will be printed, if it found the start and end point

    if ret_start == 1 and ret_end == 1:

        if flag == 0:
            start = (int(round(start_y/20)), int(round(start_x)/20))
            end = (int(round(end_y/20)), int(round(end_x)/20))
            print("end :", end,"start", start)

            ### capture the image when it finds the path
            captured = Img_process_gird.capture(ros_data)
            ### find path by using a*algorithm
            route_send, route_draw = solve.astar(start, end, grid)
            ### will be printed if no any path has found
            if(route_draw == False):
                print("No path")
                return 0
            ### i dont know what it is
            route_draw+=[start]
            route_draw=route_draw[::-1]
            final_path = Int32MultiArray(data = route_send)
            ### Publish the Path
            pub.publish(final_path)

            flag = 1

            ####  cv2.imshow  ####
            # if len(route_draw)>0:
            #     for i in range(0, len(route_draw)):
            #         cv2.circle(grid, route_draw[i], 1, (0,0,255), 1)
            # cv2.imshow('img', grid)
            # cv2.waitKey(1) & 0xFF
            ####  To Plot the frame  ####
            # xc,yc=line(route_draw)
            # fig,ax=plt.subplots()
            # ax.imshow(grid,cmap=plt.cm.Spectral)
            # ax.plot(yc,xc,color="black")
            # ax.scatter(start[1],start[0])
            # ax.scatter(end[1],end[0])
            # plt.show()


        if flag == 1:
            interruption = Img_process_gird.interrupt_detection(captured, image_np, route_draw)
            print("interruption", interruption)
            if interruption == 1:
                print('flag changed, interruption has occurred')
                flag = 0
            else:
                pub.publish(final_path)


if(__name__=="__main__"):
    sub = rospy.Subscriber('/usb_cam/image_raw/compressed', CompressedImage, finding_path)
    rospy.spin()