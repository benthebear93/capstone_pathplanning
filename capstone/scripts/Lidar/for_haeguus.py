#!/usr/bin/env python

import rospy
import numpy as np
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String, Int32, Float32, Bool
import averaged_env

rospy.init_node('lidar_mapping')
pub = rospy.Publisher('/mapping_result',LaserScan ,queue_size=1000)
# pub = rospy.Publisher('/under_meters', LaserScan, queue_size=1000)

def slice_in_list(changed_ros):
    global lst
    j=0
    for i in range(0,360,10):
        lst[j] = changed_ros[i:i+10]
        j += 1
    # print(lst)
    return lst

def normalize(hello):
    k = [0]*36
    # print(type(hello))
    for i in range(0,36):
        for j in range(0,10):
            # print(hello[i][j])
            k[i] += hello[i][j]
        k[i] = k[i]/1
    return k

def difference(ros_data):
    global prev
    changed_ros = list(ros_data.ranges)
    a = slice_in_list(changed_ros)
    d = normalize(a)
    if prev != d:
        print("different")
        for a in range(0,36):
            if prev[a] == 0:
                print "division error"
            else:
                # print "temp_one[a]",d[a]
                # print "romal_val[a]",prev[a]
                changed_par = abs((d[a]-prev[a])/prev[a])*100 #calcuate changed parcentage        
                # print("changed_par",changed_par)
        prev = d

if __name__ == '__main__':
    global lst
    global prev
    prev = [0] * 36
    lst = [[0]]*36

    sub = rospy.Subscriber('/scan', LaserScan, difference, queue_size = 1000)
    
    rospy.spin()