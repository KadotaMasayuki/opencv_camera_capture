#-------------------------------------------------------------------------------
# Name:        camera_capture
# Purpose:     カメラで撮影して保存
#
# Author:      kadota masayuki
#
# Created:     2020/04/07
# Copyright:   (c) kadota masayuki 2020
# Licence:     BSD Licence
#-------------------------------------------------------------------------------

import sys
import cv2
import time
import datetime
import os
import numpy as np
import subprocess


exportDir = "export/"

def main():
    saved = False
    angle = 0.0
    scale = 1.0
    shiftx = 0
    shifty = 0
    contrast = 1
    brightness = 0
    blurKernel = 1
    medianBlurKernel = 1
    flip = 1
    while (True):
        ret, frame = cap.read()
        h, w = frame.shape[:2]
        # 左右反転
        if (flip == 1):
            frame = cv2.flip(frame, 1) # 0:上下反転, 正の値:左右反転, 負の値:上下左右反転
        # 回転、拡大、移動
        if ((angle != 0) or (scale != 1.0) or (shiftx != 0) or (shifty != 0)):
            center = (int(w/2) + shiftx, int(h/2) + shifty)
            rotationMatrix = cv2.getRotationMatrix2D(center, angle, scale)
            frame = cv2.warpAffine(frame,
                                  rotationMatrix,
                                  (w, h),
                                  flags=cv2.INTER_LINEAR)
        # median blur
        if (medianBlurKernel > 1):
            frame = cv2.medianBlur(frame, medianBlurKernel)
        # blur
        if (blurKernel > 1):
            frame = cv2.blur(frame, ksize=(blurKernel, blurKernel))
        # コントラスト、明るさの調整
        frame = contrast * frame + brightness
        frame = np.clip(frame, 0, 255).astype(np.uint8)
        # 表示
        frame2 = frame.copy()
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame2, "exit : q,ESC      save : 1 {0}     flip : 2".format("(Saved)" if saved else ""), (10, 30), font, 0.7, (0,0,255), 1, cv2.LINE_AA)
        cv2.putText(frame2, "angle       ={0:0.1f} : y,b,g".format(angle), (10, 60), font, 0.7, (0,0,255), 1, cv2.LINE_AA)
        cv2.putText(frame2, "scale       ={0:0.1f} : u,n".format(scale), (10, 90), font, 0.7, (0,0,255), 1, cv2.LINE_AA)
        cv2.putText(frame2, "shift       =({0}, {1}) : i,j,m,k".format(shiftx, shifty), (10, 120), font, 0.7, (0,0,255), 1, cv2.LINE_AA)
        cv2.putText(frame2, "contrast    ={0:0.1f} : w,z,a".format(contrast), (10, 150), font, 0.7, (0,0,255), 1, cv2.LINE_AA)
        cv2.putText(frame2, "brightness  ={0:0.1f} : e,x,s".format(brightness), (10, 180), font, 0.7, (0,0,255), 1, cv2.LINE_AA)
        cv2.putText(frame2, "blur        ={0:d} : r,c,d".format(blurKernel), (10, 210), font, 0.7, (0,0,255), 1, cv2.LINE_AA)
        cv2.putText(frame2, "median blur ={0:d}: t,v,f".format(medianBlurKernel), (10, 240), font, 0.7, (0,0,255), 1, cv2.LINE_AA)
        cv2.imshow('img1', frame2)
        #
        saved = False
        k = cv2.waitKey(1) & 0xff
        if (k == 27 or k == ord('q')): # ESC
            break
        elif(k == ord('1')): # save
            nowtime = time.time()
            nowdate = datetime.datetime.fromtimestamp(nowtime)
            path = '{0:%Y%m%d-%H%M%S}-{1}.png'.format(nowdate, int((nowtime % 1) * 10))
            cv2.imwrite(exportDir + path, frame)
            saved = True
        elif(k == ord('2')): # flip
            flip = (flip + 1) % 2
        elif(k == ord('w')): # contrast up
            contrast += 0.1
        elif(k == ord('z')): # contrast up
            contrast -= 0.1
        elif(k == ord('a')): # contrast reset
            contrast = 1
        elif(k == ord('e')): # brightness up
            brightness += 5
        elif(k == ord('x')): # brightness down
            brightness -= 5
        elif(k == ord('s')): # brightness reset
            brightness = 0
        elif(k == ord('r')): # blur up
            blurKernel += 2
        elif(k == ord('c')): # blur down
            blurKernel -= 2
            if (blurKernel < 1):
                blurKernel = 1
        elif(k == ord('d')): # blur reset
            blurKernel = 1
        elif(k == ord('t')): # median blur up
            medianBlurKernel +=2
        elif(k == ord('v')): # median blur down
            medianBlurKernel -=2
            if (medianBlurKernel < 1):
                medianBlurKernel = 1
        elif(k == ord('f')): # median blur reset
            medianBlurKernel = 1
        elif(k == ord('y')): # rotate ccw
            angle += 0.5
            if (angle > 360):
                angle -= 360
        elif(k == ord('b')): # rotate cw
            angle -= 0.5
            if (angle < 0):
                angle += 360
        elif(k == ord('g')): # rotate reset
            angle = 0
        elif(k == ord('u')): # zoom in
            scale += 0.25
        elif(k == ord('n')): # zoom out
            scale -= 0.25
            if (scale < 0):
                scale = 0.1
        elif(k == ord('h')): # zoom reset
            scale = 1.0
        elif(k == ord('i')): # frame up
            shifty -= 10
            if (abs(shifty) >= h):
                shifty = -1 * (h - 10)
        elif(k == ord('j')): # frame left
            shiftx -= 10
            if (abs(shiftx) >= w):
                shiftx = -1 * (w - 10)
        elif(k == ord('m')): # frame down
            shifty += 10
            if (shifty >= h):
                shifty = h - 10
        elif(k == ord('k')): # frame right
            shiftx += 10
            if (shiftx >= w):
                shiftx = w - 10
        

if __name__ == '__main__':
    # パス設定
    exportDir = os.path.dirname(os.path.abspath(__file__)) + "/" + exportDir
    print(exportDir)
    if not os.path.isdir(exportDir):
        os.makedirs(exportDir)
    # カメラID、画素数(幅、高さ)、フレームレートをコマンドラインから読み取る
    #   画素数とフレームレートはオプション
    args = sys.argv
    if (len(args) < 2):
#        raise("カメラ番号を指定して起動してください\n  command  <Camera> [ <Width>  <Height> [ <fps> ] ]")
        raise("カメラ番号を指定して起動してください\n  command  <Camera>")
    devId = int(args[1])
#    if (len(args) >= 4):
#        width = int(args[2])
#        height = int(args[3])
#    if (len(args) >= 5):
#        fps = int(args[4])
    # カメラ起動
    cap = cv2.VideoCapture(devId)
    # 画素数(幅、高さ)、フレームレートを設定する
    #   設定された値が返ってくる
#    fps, width, height = setFpsWidthHeight(fps, width, height)
    main()
    # あとしまつ
    cap.release()
    cv2.destroyAllWindows()
