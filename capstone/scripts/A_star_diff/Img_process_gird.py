#!/usr/bin/env python2
import cv2
import numpy as np

class gridmaker:
    def __init__(self,s,frame):
        self.s=s
        self.img = frame
        #self.img=cv2.imread("/home/benlee/catkin_ws/src/find_path/script/A_star_diff/frame.jpg",0)  #bring image
        self.h,self.w=self.img.shape #get image size h = height, w = width
        self.grid=np.zeros(shape=(26,32)) #make blank zero numpy 

    def iswhite(self,a,b,block): # a = w, b = h, block = img 
        h,w=block.shape
        count=0
        for i in range(b,b+20):
            for j in range(a,a+20):
                if(i<480 and j<640):
                    if(block[i][j]>0): # >0 = 1 , means there is obstacle!!
                        count=count+1
                        #print("count", count)  
        if(count>225):
            return True
        return False


    def returnGrid(self):
        for i in range(0,self.w,self.s):
            for j in range(0,self.h,self.s):
                if(self.iswhite(i,j,self.img)):
                    self.grid[int(j/self.s)][int(i/self.s)]=1
                    #print(self.grid[int(j/self.s)][int(i/self.s)])
                    #cv2.rectangle(frame,(i,j),(i+self.s,j+self.s),(255,0,0),-1)
                #else:
                    #cv2.rectangle(frame,(i,j),(i+self.s,j+self.s),(255,0,0),1)

        return self.grid

class Basic_map:
    def __init__(self):
        self.Color_HSV = {}
        self.Color_HSV['RED'] = [126, 134, 0, 255, 255, 255]
        self.Color_HSV['YELLOW'] = [0, 65, 60, 40, 152, 255]
        self.Color_HSV['GREEN'] = [59, 61, 60, 100, 255, 255]

        self.x = 0
        self.y = 0
        return
    def Gmask_for_start_end(self,img,color):
        lowerBound = np.array(self.Color_HSV[color][:3])
        upperBound = np.array(self.Color_HSV[color][3:6])
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        color_mask = cv2.inRange(hsv, lowerBound, upperBound)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        erosion = cv2.erode(color_mask, kernel,iterations =1)
        dilation = cv2.dilate(erosion, kernel, iterations=3)
        return dilation

    def find(self,img, color): #find specific color points, in this case start, end_nodes
        lowerBound = np.array(self.Color_HSV[color][:3])
        upperBound = np.array(self.Color_HSV[color][3:6])
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        color_mask = cv2.inRange(hsv, lowerBound, upperBound)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        erosion = cv2.erode(color_mask, kernel,iterations =1)
        dilation = cv2.dilate(erosion, kernel, iterations=3)
        # frame=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # th,frame=cv2.threshold(frame,127,255,cv2.THRESH_BINARY)
        _, contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            for i in range(len(contours)):
                # Get area value
                area = cv2.contourArea(contours[i])
                print("area",area)
                if area > 0:  # minimum  area
                    rect = cv2.minAreaRect(contours[i])
                    (self.x, self.y), (w, h), angle = cv2.minAreaRect(contours[i])
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    #cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
                    return True, round(self.x), round(self.y), w, h,dilation
                else:
                    return False, 0, 0, 0, 0, dilation
        else:
            return False, 0, 0, 0, 0, dilation

    def obstacle_load(self,img): # make base_map that has obstacle pixel data
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, base_map = cv2.threshold(img_gray, 72, 255, 1)
        return base_map


def capture(ros_data):
    np_arr = np.fromstring(ros_data.data, np.uint8)
    image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    frame = image_np
    # cv2.imwrite('frmae.jpg', frame)
    # cv2.waitKey(1) & 0xFF
    return frame

def interrupt_detection(captured, current, path):
    count = 0
    for (first, last) in path:
        for i in range(0,3):
            ####  Difference between Captured vs. Current Frame 
            if captured[first][last][i]!=current[first][last][i]:
                count = count + 1
            else:
                count = count
    if count >= 18:
        return 1
    else:
        return 0