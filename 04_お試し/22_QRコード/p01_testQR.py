# -*- coding: utf-8 -*-
"""
Created on Thu May 28 15:07:44 2020

@author: p000495138
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image, ImageFilter
import qrcode


#QRコード生成
img_out = qrcode.make('test text')
img_out.save('result/qrcode_test.png')


#QRコード読み込み
img_in = Image.open('source/d03.bmp')
data   = decode(img_in)
df     = pd.DataFrame(data)
plt.imshow(img_in)

for index, row in df.iterrows():
    print(row["data"])


