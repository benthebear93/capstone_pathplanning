#!/usr/bin/env python2

import sys
import cv2
import math
import numpy as np

def resize(obstacle):
    img = obstacle
    #temp_img =img.copy()
    pixel_chg_img = []
    grid_resize = 0
    for k in range(0,399,4): # 0,2,4 so on (*for step)
        mask_average = 0
        resize_img = []
        for j in range(0,399,4):
            mask_average_one = int(img[k][j]) + int(img[k][j+1]) + int(img[k][j+2]) + int(img[k][j+3])
            mask_average_two = int(img[k+1][j]) + int(img[k+1][j+1]) + int(img[k+1][j+2]) + int(img[k+1][j+3])
            mask_average_three = int(img[k+2][j]) + int(img[k+2][j+1]) + int(img[k+2][j+2]) + int(img[k+2][j+3])
            mask_average_four = int(img[k+3][j]) + int(img[k+3][j+1]) + int(img[k+3][j+2]) + int(img[k+3][j+3])
            mask_average = mask_average_one + mask_average_two + mask_average_three + mask_average_four
            if mask_average == 0:
                resize_img.append(0)
            else:
                resize_img.append(255)
        pixel_chg_img.append(resize_img)
        grid_resize = np.asarray(pixel_chg_img, dtype=np.uint8)
    return grid_resize


def convert2grid(img, height, width, x, y):
    ### initalize
    grid_x = grid_y = 0
    resized_grid_image = stacked_pixel = []
    ### make the mobile robot pixel to square
    if(height > width):
        width = height
        if (width%2) != 0:
            width = width + 1
    else:
        if (width%2) != 0:
            width = width + 1
    pixel_size = width

    ### starting pixel of the mobile robot pixel (left edge)
    x, y = x - pixel_size/2, y - pixel_size/2

    while True:
        if (x - pixel_size) >= 0:
            grid_x = x - pixel_size
            x = grid_x
        elif (y - pixel_size) >= 0:
            grid_y = y - pixel_size
            y = grid_y
        else:
            if(grid_x == 0 and grid_y == 0):
                break
            grid_x = grid_x - pixel_size
            grid_y = grid_y - pixel_size
            break
    original_grid_x = grid_x
    original_grid_y = grid_y

    while True:
        for i in range(0, int(pixel_size)):
            for j in range(0, int(pixel_size)):
            	mask = img[grid_x+i][grid_y+j]
                # if img[x+i][y+j][0] < 255 and img[x+i][y+j][1] <255 and img[x+i][y+j][2] < 255:

        if mask == 0:
        	stacked_pixel.append(0)
        else:
        	stacked_pixel.append(255)

        if grid_x < img.shape[0]:
            grid_x = grid_x + pixel_size
        else:
            grid_x = original_grid_x
            grid_y = grid_y + pixel_size
            resized_grid_image.append([stacked_pixel])
            stacked_pixel = []

        if gird_x < img.shape[0] and grid_y < img.shape[1]:
            break



    return start, grid