######   it was in the line 21 in python file mapping.py    ######

# def discrimination_of_difference_point1(ros_data):
# 	global temp
# 	# print(len(ros_data.ranges))
# 	lists = list(ros_data.ranges)
# 	print('-----------------------------------------------')
# 	# if temp != ros_data.ranges:
# 	if temp != lists:
# 		diff = set(lists) - set(temp)  ##difference between prev scan_value
# 		# print(len(diff))
# 		# print(type(list(diff)))
# 		for numbers in list(diff):  
# 			a = lists.index(numbers)   ## a = position of the changed postion data
# 			# print(a)
# 			lists[a] = 0
# 		temp = ros_data.ranges
# 	# print(len(ros_data.ranges))
# 	# ros_data.ranges = diff
# 	ros_data.ranges = lists
# 	pub.publish(ros_data)


# def discrimination_of_difference_point2(ros_data):
# 	global storage
# 	# print(len(ros_data.ranges))
# 	lds_ranges = list(ros_data.ranges)
# 	print('-----------------------------------------------')
# 	# if temp != ros_data.ranges:
# 	for i in range(0,360):
# 		if (storage[i]-lds_ranges[i])<0.005 :
# 			lds_ranges[i] = 0
# 		else:
# 			print("different")
# 	storage = ros_data.ranges
# 	ros_data.ranges = lds_ranges
# 	pub.publish(ros_data)