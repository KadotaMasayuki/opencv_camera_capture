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
    beginTime = 0
    nowTime = 0;
    isRecording = False
    isFlip = False
    while (True):
        ret, frame = cap.read()
        nowTime = time.time()
        # 左右反転
        if (isFlip):
            frame = cv2.flip(frame, 1) # 0:上下反転, 正の値:左右反転, 負の値:上下左右反転
        # 動画を1フレームずつ保存
        if (isRecording):
            video.write(frame)
        # 表示
        font = cv2.FONT_HERSHEY_SIMPLEX
        if (isRecording):
            # 記録中は赤枠を表示
            cv2.rectangle(frame, (0+1,0+1), (w-2,h-2), (0, 64, 255), 4, cv2.LINE_8)
            # メニュー
            cv2.putText(frame, "Recording       <1>stop   <2>flip   <q,ESC>exit", (10, 30), font, 0.7, (0,0,255), 1, cv2.LINE_AA)
            # 記録時間
            cv2.putText(frame, "{0:0.3f}[sec]".format(nowTime - beginTime), (10, 60), font, 0.7, (0, 0, 255), 1, cv2.LINE_AA)
        else:
            # メニュー
            cv2.putText(frame, "Not Recording   <1>record   <2>flip   <q,ESC>exit", (10, 30), font, 0.7, (0,255,0), 1, cv2.LINE_AA)
        cv2.imshow('video_capture', frame)

        k = cv2.waitKey(1) & 0xFF
        if (k == 27 or k == ord('q')):        # ESCキーまたはqキーでループを抜ける
            break
        elif (k == ord('1')):
            isRecording = not isRecording
            if (isRecording):
                # ファイル名に日時を使用
                beginTime = nowTime
                nowDate = datetime.datetime.fromtimestamp(beginTime)
                filePath = exportDirectoryPath + os.path.sep + '{0:%Y%m%d-%H%M%S}-{1}.mp4'.format(nowDate, int((nowTime % 1) * 10))
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

