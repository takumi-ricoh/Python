#パブリッシャ

import paho.mqtt.client as mqtt
from time import sleep

#%% ブローカに接続できたときの処理
def on_connect(client, userdata, flag, rc):
    print("コードとつながったよ：" + str(rc))


#%% ブローカが切断した時の処理
def on_disconnect(client, userdata, flag, rc):
    if rc != 0:
        print("意図しない切断")


#%% publishが完了したときの処理
def on_publish(client, userdata, mid):
    print("パブリッシュ：{0}".format(mid))

#%% メイン関数
def main():
    client = mqtt.Client(clean_session=True) #インスタンス
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish

    client.connect("localhost",1883,45)

    client.loop_start() #pubはstart

    #無限ループ
    while True:
        client.publish("drone/001","Hello, Drone")
        sleep(3)

#%% 実行
if __name__ == "__main__":
    main()
