#サブスクライバ

import paho.mqtt.client as mqtt

#%% ブローカに接続できた時の処理
def on_connect(client, userdata, flag, rc):
    print("このコードとつながったよ：" + str(rc))
    client.subscribe("drone/001")

#%% ブローカが切断した時
def on_disconnect(client,userdata,flag,rc):
    if rc != 0:
        print("意図しない切断が発生")

#%% メッセージが届いた時
def on_message(client,userdata,msg):
    topic = msg.topic
    message = msg.payload
    print("受信メッセージ:" + str(message) + "トピック:" + topic)

#%% MQTTの接続設定
client = mqtt.Client() #インスタンス
client.on_connect = on_connect #接続事処理を登録
client.on_disconnect = on_disconnect #切断時処理を登録
client.on_message = on_message #受診時の処理を登録

#%% 接続
client.connect("localhost",1883,45)

client.loop_forever()
