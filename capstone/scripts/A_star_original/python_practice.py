# import Img_process
# import cv2

# def main():
#     img = cv2.imread('map_donut.jpg', cv2.IMREAD_COLOR)
#     obstacle_map = Img_process.Basic_map()
#     img = obstacle_map.obstacle_load(img)
#     # print(img)
#     x = y = mask = 0
#     stacked_pixel = resized_grid_image = []

#     while True:
#         for i in range(0, 8):
#             for j in range(0, 8):
#                 mask = mask + img[x+i][y+j]
#         print(mask)

#         if mask == 0:
#         	stacked_pixel.append(0)
#         	mask = 0
#         else:
#         	stacked_pixel.append(255)
#         	mask = 0

#         if x < img.shape[0]:
#             x = x + 8
#         else:
#             x = 0
#             y = y + 8
#             resized_grid_image.append([stacked_pixel])
#             print(stacked_pixel)
#             stacked_pixel = []

#         # print(resized_grid_image)

#         if x > img.shape[0] and y > img.shape[1]:
#             break

# if __name__ == '__main__':
# 	main()

import ros
from capstone_vision.msg import Smartfactory

rospy.init_node('hello')
pub = rospy.Publisher('pub_topic_name', Smartfactory)


if __name__ == '__main__':
	a = [(1,2),(2,3),(3,4),(4,5)]

	pub.publish(a)