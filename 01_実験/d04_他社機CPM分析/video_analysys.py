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


importname='HP_A4T.MPG'    
cap = cv2.VideoCapture(importname,0)

# フレーム数を取得する
NumOfFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(NumOfFrames)

#時系列保存データ
q=[0]
count=0

while(cap.isOpened()):

    ret, frame = cap.read()
    
    # 読めなかったら抜ける
    if ret == False:
        break    
    
    """ 画像処理  """   
    
    #カラー　→　グレースケール
    Img1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    #2値化    
    ret,Img2 = cv2.threshold(Img1,127,255,cv2.THRESH_BINARY) 
    
    """
    #勾配計算
    grad = cv2.Sobel(thresh,cv2.CV_64F,1,0,ksize=1) #ソーベルフィルタ
    #平滑化(ノイズを減らす)
    Img = cv2.GaussianBlur(grad,(3,3),0)#ガウシアンフィルタ
    """
    
    """ 時系列データに保存  """        
    x,y = [140,350] #座標
    Img3=cv2.rectangle(Img2,(y-5,x-5),(y+5,x+5),255,1) #四角形表示
    q.append(Img3[x,y]) #qに保存

    """ 動画表示 """

    cv2.imshow('frame',Img3)#表示
    
    if cv2.waitKey(1) & 0xFF == ord('q'): #押されたら終了
        break

    """        
    いろいろなフィルタがあるので使ってみて
    https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_table_of_contents_imgproc/py_table_of_contents_imgproc.html#py-table-of-content-imgproc

    ・勾配計算
    　　　　lastimg = cv2.Canny(thresh,100,110)
    
    平滑化
    　　　　#lastimg = cv2.medianBlur(grad,3)
    """
    count += 1#フレーム数カウント
    print('frame=',count)
   
cap.release()
cv2.destroyAllWindows()
#結果の保存
savename=importname+'_res.CSV'
np.savetxt(savename,q,delimiter=",", fmt='%.1f')

#画像保存
#saveimg = lastimg.astype(np.uint8)
#cv2.imwrite('lastimg.jpg',saveimg)
