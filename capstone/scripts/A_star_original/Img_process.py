#!/usr/bin/env python2
import numpy as np
import cv2


class Basic_map:
    def __init__(self):
        self.Color_HSV = {}
        # hsv 3 low , hsv 3 high
        self.Color_HSV['RED'] = [133, 122, 0, 255, 255, 255]
        #self.Color_HSV['RED'] = [200, 100, 100, 255, 155, 200]
        self.Color_HSV['BLUE'] = [70, 117, 108, 157, 255, 255]
        #self.Color_HSV['BLUE'] = [140, 120, 160, 220, 180, 255]

        self.x = 0
        self.y = 0
        return
        
    def find(self,img, color): #find specific color points, in this case start, end_nodes
        lowerBound = np.array(self.Color_HSV[color][:3])
        upperBound = np.array(self.Color_HSV[color][3:6])
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        color_mask = cv2.inRange(hsv, lowerBound, upperBound)
        #ret, thr = cv2.threshold(color_mask, 127, 255, 0)
        _, contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            for i in range(len(contours)):
                # Get area value
                area = cv2.contourArea(contours[i])
                if area > 1:  # minimum  area
                    rect = cv2.minAreaRect(contours[i])
                    (self.x, self.y), (w, h), angle = cv2.minAreaRect(contours[i])
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
                    return 1, round(self.x), round(self.y), color_mask, w, h
                else:
                    return 0, 0, 0, color_mask, 0, 0
        else:
            return 0, 0, 0, color_mask, 0, 0

    def obstacle_load(self,img): # make base_map that has obstacle pixel data
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, base_map = cv2.threshold(img_gray, 100, 255, 1)
        return base_map
