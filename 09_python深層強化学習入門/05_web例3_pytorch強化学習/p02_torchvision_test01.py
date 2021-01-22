# -*- coding: utf-8 -*-
"""
学習済み
torchvisionで人のキーポイント抽出
"""

import matplotlib.pyplot as plt
import numpy as np
import torch
import torchvision
from PIL import Image
#from chainercv.visualizations import vis_bbox, vis_point

image_path = 'torchivision_testpic3.bmp'
image = Image.open(image_path).convert('RGB')

#使用するデバイス（CPU or GPU）を指定します。
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

#学習済のKeyPoint R-CNNのモデルを読み込んでデバイスに渡します。model.eval()にてモデルのモードを推論モードに切り替えます。
model = torchvision.models.detection.keypointrcnn_resnet50_fpn(pretrained=True)
model = model.to(device)
model.eval()

#ImageオブジェクトをTensorにしてデバイスに渡します。ついでにモデルに渡す形（リスト）にしておきます。
image_tensor = torchvision.transforms.functional.to_tensor(image)
x = [image_tensor.to(device)]

#推論して、物体検出の結果・キーポイント検出の結果を取得します。
prediction = model(x)[0]
bboxes_np = prediction['boxes'].to(torch.int16).cpu().numpy()
labels_np = prediction['labels'].byte().cpu().numpy()
scores_np = prediction['scores'].cpu().detach().numpy()
keypoints_np = prediction['keypoints'].to(torch.int16).cpu().numpy()
keypoints_scores_np = prediction['keypoints_scores'].cpu().detach().numpy()


#%%　認識を四角で描画
import cv2

image2 = image.copy()

#ボックス描画
for i in bboxes_np[3:4]:
    x,y,w,h = i
    image2 = cv2.rectangle(np.int16(image2), (x,y), (x+w, y+h), (0, 0, 255), thickness=10)

#キーポイント描画



plt.imshow(image2)