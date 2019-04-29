#!/usr/bin/env python

# - Mobile Robot -
#	size : 0.08m * 0.16m
# - Lidar01 -
#	Detection Distance(Range) : 120mm(0.12m) ~ 3500mm(3.5m)
#	Scan Rate : 300rpm(10rpm)
# - obstacles -
# 	Can be Ignored Size(Length/Depth): 0.06m

import rospy
import numpy as np
import math
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String, Int32, Float32, Bool

rospy.init_node('lidar_mapping')
pub = rospy.Publisher('/mapping_result', LaserScan, queue_size=1000)
# 2pub_mrobot = rospy.Publisher('/mobile_robot', LaserScan, queue_size=100)

# def test(ros_data):
	# ###  return_raw_ros_data_to_check_ros_data  ###
	# raw_topic_data = ros_data
	# pub.publish(raw_topic_data)
	# return raw_topic_data

	# ###  publish_circular_view_in_rviz ###
	# global temp
	# t1 = [1]
	# ros_data.ranges = t1 * 360
	# pub.publish(ros_data)

	# ###  make tuple to list  ###
	# lists = list(ros_data.ranges)
	# print(lists)

# def identify_mrobot(ros_data):

# def env(ros_data, stacked, n):
# 	global avg
# 	for i in range(0,360):
# 		avg[i] = (ros_data[i] + stacked[i]) / n
# 		stacked[i] = stacked[i] + ros_data[i]
# 	return avg, stacked

def visualize_env_with_mobstacle(ros_data):    ## mobstacle = moving obstacle
	global storage, stacked, n
	global avg
	avg = [0]*360
	lds_ranges = list(ros_data.ranges)

	## option 1
	# avg, stacked = env(lds_ranges, stacked, n)  ## avg = env, stacked = sum of the sensored data
	# n += 1
	# print(n)

	## option 2
	if n >= 50:  ## after averaging env with 50times
		del storage[0]
		# avg, stacked = env(lds_ranges, stacked, n)  ## avg = env, stacked = sum of the sensored data
		storage.append([stacked])
		print(n)
	else:
		storage.append()
		# avg, stacked = env(lds_ranges, stacked, n)  ## avg = env, stacked = sum of the sensored data
		print("data(environment) is not setted up yet (rotation =", n,"under 50.")
		n+=1

	ros_data.ranges = avg
	pub.publish(ros_data)

if __name__ == '__main__':
	global temp, stacked, storage
	global n

	n = 2
	temp = [0] * 360
	storage = []
	stacked = temp

	sub = rospy.Subscriber('/scan', LaserScan, visualize_env_with_mobstacle, queue_size = 1000)
	# rospy.Subscriber('/scan', LaserScan, check_coordinate, queue_size = 100)
	rospy.spin()


