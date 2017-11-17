# -*- coding: utf-8 -*-
"""
使い方
　・動画データとこのプログラムを同じフォルダにいれる
　・File　exploreでそのフォルダに移動
　・座標(33行目)　を指定
　・プログラムを実行
　・結果のｑをエクセルで処理する
"""

import numpy as np #数値計算
import cv2 #OpenCV
import matplotlib.pyplot as plt

#name = 'ユニット内の様子.avi'
name = 0 #USBカメラ
cap = cv2.VideoCapture(name)

#カメラ検出サイズ
cap.set(cv2.CAP_PROP_FRAME_WIDTH ,160)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT ,120)
#cap.set(cv2.CAP_PROP_FOURCC ,cv2.FOURCC('B','G','R',3))

#動体検出
MOG2 = cv2.createBackgroundSubtractorMOG2()#
KNN = cv2.createBackgroundSubtractorKNN()#

#顔検出
face_cascade = cv2.CascadeClassifier(['haarcascade_frontalface_default.xml'])
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

while(cap.isOpened()):
    ret, frame0 = cap.read()

    #サイズ変更
    frame0=cv2.resize(frame0,(160,120))
  
    # 読めなかったら抜ける
    if ret == False:
        break    
    
    #モノクロ
    frame1=cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY)
    frame2=cv2.cvtColor(frame1, cv2.COLOR_GRAY2BGR)#次元を揃えるためにBGRに戻す

    #2値化
    ret2,frame3=cv2.threshold(frame2,150,255,cv2.THRESH_BINARY)
        
    #ガウシアンブラー
    frame4 = cv2.GaussianBlur(frame2,(5,5),0)#ガウシアンフィルタ    
    
    #ソーベルフィルタ
    frame5 = cv2.Sobel(frame2,cv2.CV_64F,1,0,ksize=1) #ソーベルフィルタ
    
    #hariss
    temp=np.float32(frame1)
    frame6=cv2.cornerHarris(temp,2,3,0.01)#ハリスコーナー
    frame6=cv2.cvtColor(frame6, cv2.COLOR_GRAY2BGR)

    #canny
    frame7=cv2.Canny(frame2,100,100)   
    frame7=cv2.cvtColor(frame7, cv2.COLOR_GRAY2BGR)  

    #回転(アフィン変換）
    center = tuple(np.array([frame0.shape[1] * 0.5, frame0.shape[0] * 0.5]))# 今回は画像サイズの中心をとっている
    size = tuple(np.array([frame0.shape[1], frame0.shape[0]]))# 画像サイズの取得(横, 縦)
    angle = -110.0# 回転させたい角度    # ラジアンではなく角度(°)
    scale = 1.5# 拡大比率
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)# 回転変換行列の算出
    frame8 = cv2.warpAffine(frame0, rotation_matrix, size, flags=cv2.INTER_CUBIC)# アフィン変換
    
    
    #動体検出1
    frame9 = MOG2.apply(frame0)
    frame9=cv2.cvtColor(frame9, cv2.COLOR_GRAY2BGR)  
    
    #動体検出2
    frame10 = KNN.apply(frame0)
    frame10=cv2.cvtColor(frame10, cv2.COLOR_GRAY2BGR)  
    
    #顔検出
    frame11=frame2.copy()
    faces = face_cascade.detectMultiScale(frame11 ,1.3, 5)
    for (x,y,w,h) in faces:
        frame11 = cv2.rectangle(frame11,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = frame11[y:y+h, x:x+w]
        roi_color = frame11[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    #複数表示
    both1=np.hstack((frame0,frame2,frame3,frame4))
    both2=np.hstack((np.uint8(frame5),np.uint8(frame6),frame7,frame8))
    both3=np.hstack((frame9,frame10,frame11,frame0))
    both = np.vstack((both1,both2,both3))
    
    cv2.imshow('raw/gray/mono/gauss/#sobel/harris/Canny/Rotate/#MOG2/KNN/cascade',both)#表示
    
    if cv2.waitKey(1) & 0xFF == ord('q'): #押されたら終了
        break

cap.release()
cv2.destroyAllWindows()
