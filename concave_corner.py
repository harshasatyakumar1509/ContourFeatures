import cv2
import matplotlib.pyplot as plt
import numpy as np

path = "/Users/sriharsha/Documents/Agricx/rice_defects/kStTn.jpg"
img = cv2.imread(path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 125, 255, cv2.THRESH_BINARY_INV)


_, noisy_contours, hierarchy = cv2.findContours(thresh,cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
test_canvas = np.zeros_like(thresh)
noisy_contours = np.asarray(noisy_contours)
for e,cnt in enumerate(noisy_contours):
    cv2.drawContours(test_canvas, [cnt],0 , 255,1)