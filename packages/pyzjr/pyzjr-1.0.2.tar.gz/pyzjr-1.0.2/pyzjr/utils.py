import cv2
import math
import numpy as np
import os, shutil
from matplotlib import pyplot as plt

def getContours(img, cThr=(100, 100), showCanny=False, minArea=1000, filter=0, draw=True):
    """
    :param img: 输入图像
    :param cThr: 阈值
    :param showCanny:展示经过处理后的边缘,默认Fales
    :param minArea: 更改大小
    :param filter: 过滤
    :param draw: 绘制边缘
    :return: 返回图像轮廓
    """
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, cThr[0], cThr[1])
    kernel = np.ones((5, 5))
    imgDial = cv2.dilate(imgCanny, kernel, iterations=3)
    imgThre = cv2.erode(imgDial, kernel, iterations=2)
    if showCanny: cv2.imshow('Canny', imgThre)
    contours, hiearchy = cv2.findContours(imgThre, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    finalCountours = []
    for i in contours:
        area = cv2.contourArea(i)
        if area > minArea:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            bbox = cv2.boundingRect(approx)
            if filter > 0:
                if len(approx) == filter:
                    finalCountours.append([len(approx), area, approx, bbox, i])
            else:
                finalCountours.append([len(approx), area, approx, bbox, i])
    finalCountours = sorted(finalCountours, key=lambda x: x[1], reverse=True)
    if draw:
        for con in finalCountours:
            cv2.drawContours(img, con[4], -1, (0, 0, 255), 3)
    return img, finalCountours


def empty(a):
    pass

def RemoveInboxes(boxes):
    """
    中心点的方法,去除重叠的框,并去掉相对较小的框
    :param boxes: [minc, minr, maxc, maxr]
    :return: 过滤的boxes
    """
    final_boxes = []
    for box in boxes:
        x1, y1, x2, y2 = box
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        box_area = (x2 - x1) * (y2 - y1)
        is_inner = False
        for fb in final_boxes:
            fx1, fy1, fx2, fy2 = fb
            if fx1 <= cx <= fx2 and fy1 <= cy <= fy2:
                fb_area = (fx2 - fx1) * (fy2 - fy1)
                if box_area >= fb_area:
                    final_boxes.remove(fb)
                else:
                    is_inner = True
                    break
        if not is_inner:
            final_boxes.append(box)
    return final_boxes