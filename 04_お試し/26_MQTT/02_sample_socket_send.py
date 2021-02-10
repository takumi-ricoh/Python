from socket import socket, AF_INET, SOCK_STREAM
import random
import time

HOST        = 'localhost'
PORT        = 1883#51000

CHR_CAN     = '\18'
CHR_EOT     = '\04'

def com_send(mess):

    while True:
        try:
            # 通信の確立
            sock = socket(AF_INET, SOCK_STREAM)
            sock.connect((HOST, PORT))

            # メッセージ送信
            sock.send(str(random.random()).encode('utf-8'))
            #sock.send(mess.encode('utf-8'))

            # 通信の終了
            #sock.close()
            #break
            time.sleep(2)

        except:
            print ('retry: ' + mess)


def proc():
    com_send('message test')

def exit():
    com_send(CHR_EOT)

def cancel():
    com_send(CHR_CAN)

proc()