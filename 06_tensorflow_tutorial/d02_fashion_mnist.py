# -*- coding: utf-8 -*-
"""
Created on Wed May 29 17:08:48 2019

@author: p000495138
"""

import tensorflow as tf
from tensorflow import keras

#ヘルパライブラリ
import numpy as np
import matplotlib.pyplot as plt

print(tf.__version__)


### add for TensorBoard
#from tensorflow.keras import callbacks
#from tensorflow.keras import backend.tensorflow_backend as KTF
#
#old_session = KTF.get_session()
#
#session = tf.Session('')
#KTF.set_session(session)
#KTF.set_learning_phase(1)
### 


#%%データのロード
fashion_mnist = keras.datasets.fashion_mnist
(train_images,train_labels),(test_images, test_labels) = fashion_mnist.load_data()

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

#%%データスケーリング
train_images = train_images / 255.0
test_images = test_images / 255.0


#%%ニュ＾ラルネット作成
model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28,28)),
        keras.layers.Dense(128, activation=tf.nn.relu),
        keras.layers.Dropout(rate=0.3),
        keras.layers.Dense(128, activation=tf.nn.relu),
        keras.layers.Dense(10,activation=tf.nn.softmax)])

model.compile(optimizer=tf.keras.optimizers.Adam(),
              loss= 'sparse_categorical_crossentropy',
              metrics=['accuracy'])


#%%tensorboardへ追加
#tb_cb = keras.callbacks.TensorBoard(log_dir="~/logs/", histogram_freq=1)
#cbks = [tb_cb]

#%%学習
model.fit(train_images, train_labels, epochs=5)

#%%精度検証
test_loss, test_acc = model.evaluate(test_images, test_labels)
print('Test accuracy:', test_acc)

#%%予測する
predictions = model.predict(test_images)
print("\nraw_result:\n",predictions[0])
print("\nresult:\n",class_names[np.argmax(predictions[0])])
print("\ncorrect:\n",class_names[test_labels[0]])

### add for TensorBoard
#KTF.set_session(old_session)
###
#%%プロット

#画像表示
def plot_image(i, predictions_array, true_label, img):
    predictions_array, true_label, img = predictions_array[i], true_label[i], img[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    
    plt.imshow(img, cmap=plt.cm.binary)
    
    predicted_label = np.argmax(predictions_array)
    if predicted_label == true_label:
        color='blue'
    else:
        color='red'
    plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                   100*np.max(predictions_array),
                                   class_names[true_label]),color=color)

#
def plot_value_array(i, predictions_array, true_label,):
    predictions_array, true_label, = predictions_array[i], true_label[i], 
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    thisplot = plt.bar(range(10), predictions_array, color="#777777")
    plt.ylim([0,1])
    predicted_label = np.argmax(predictions_array)
    
    thisplot[predicted_label].set_color('red')
    thisplot[true_label].set_color('blue')

#15個のデータについて表示
num_rows=5
num_cols=3
num_images=num_rows*num_cols
plt.figure(figsize=(2*2*num_cols, 2*num_rows))
for i in range(num_images):
    plt.subplot(num_rows, 2*num_cols, 2*i+1)
    plot_image(i+10,predictions, test_labels, test_images)
    plt.subplot(num_rows, 2*num_cols, 2*i+2)
    plot_value_array(i+10, predictions, test_labels)

#1個のデータについて詳細表示
img = test_images[0]
print(img.shape)

#tensorflowに合わせて次元を増やす
img2 = (np.expand_dims(img,0))
print(img2.shape)
    
predictions_single = model.predict(img2)
print(predictions_single)

plot_value_array(0, predictions_single, test_labels)
plt.xticks(range(10), class_names, rotation=45)
#%%表示
#plt.figure(figsize=(10,10))
#for i in range(36):
#    plt.subplot(5,5,i+1)
#    plt.xticks([])
#    plt.yticks([])
#    plt.grid(False)
#    plt.imshow(train_images[i],cmap=plt.cm.binary)
#    plt.xlabel(class_names[train_labels[i]])
    