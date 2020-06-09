#-------------------------------------------------------------------------------
# Name:        camera_capture
# Purpose:     カメラで撮影して動画として保存
#
# Author:      kadota masayuki
#
# Created:     2020/06/08
# Copyright:   (c) kadota masayuki 2020
# Licence:     BSD Licence
#-------------------------------------------------------------------------------

import cv2
import sys
import os
import time
import datetime


exportDirectoryName = "export"


if __name__ == '__main__':
    # パス設定
    exportDirectoryPath = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + exportDirectoryName
    print("exportDir={0}".format(exportDirectoryPath))
    if not os.path.isdir(exportDirectoryPath):
        os.makedirs(exportDirectoryPath)

    # カメラIDをコマンドラインから入力
    args = sys.argv
    if (len(args) < 2):
        raise("カメラ番号を指定して起動してください\n  command  <Camera>")
    devId = int(args[1])
    cap = cv2.VideoCapture(devId)                               # カメラCh.(ここでは0)を指定

    # 動画ファイル保存用の設定
    fps = int(cap.get(cv2.CAP_PROP_FPS))                    # カメラのFPSを取得
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))              # カメラの横幅を取得
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))             # カメラの縦幅を取得
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')        # 動画保存時のfourcc設定（mp4用）
    print(" {0} fps".format(fps))
    print(" ({0}, {1})".format(w, h))
    print(" fourcc=mp4v")
    print(" {0}".format(fps))

    # 撮影＝ループ中にフレームを1枚ずつ取得（qキーで撮影終了）
    isRecording = False
    isFlip = False
    while (True):
        ret, frame = cap.read()
        # 左右反転
        if (isFlip):
            frame = cv2.flip(frame, 1) # 0:上下反転, 正の値:左右反転, 負の値:上下左右反転
        # 動画を1フレームずつ保存
        if (isRecording):
            video.write(frame)
        # 表示
        font = cv2.FONT_HERSHEY_SIMPLEX
        if (isRecording):
            cv2.putText(frame, "Recording       <1>stop    <2>flip    <q,ESC>exit", (10, 30), font, 0.7, (0,0,255), 1, cv2.LINE_AA)
        else:
            cv2.putText(frame, "Not Recording   <1>record    <2>flip    <q,ESC>exit", (10, 30), font, 0.7, (0,0,255), 1, cv2.LINE_AA)
        cv2.imshow('video_capture', frame)

        k = cv2.waitKey(1) & 0xFF
        if (k == 27 or k == ord('q')):        # ESCキーまたはqキーでループを抜ける
            break
        elif (k == ord('1')):
            isRecording = not isRecording
            if (isRecording):
                # ファイル名に日時を使用
                nowtime = time.time()
                nowdate = datetime.datetime.fromtimestamp(nowtime)
                filePath = exportDirectoryPath + os.path.sep + '{0:%Y%m%d-%H%M%S}-{1}.mp4'.format(nowdate, int((nowtime % 1) * 10))
                video = cv2.VideoWriter(filePath, fourcc, fps, (w, h))  # 動画の仕様（ファイル名、fourcc, FPS, サイズ）
                print("  >record start:{0}".format(filePath))
            else:
                video.release()  # 動画保存を終了
                print("  >record end")
        elif (k == ord('2')):
            isFlip = not isFlip

    # あとしまつ
    camera.release()
    cv2.destroyAllWindows()

