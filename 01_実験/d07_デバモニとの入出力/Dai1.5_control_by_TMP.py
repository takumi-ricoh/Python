# -*- coding: utf-8 -*-
"""
Spyderエディタ

１．TMPにより、エンジンログから状態遷移を読み取る
２．印刷前になったら当接、待機になったら離間する
３．同時に、gpio8から、high/low信号を出して、NR-500にタイミングを認識させる

"""

from serial import Serial
import ctypes
import time

PORT1 = "COM18"
PORT2 = "COM19"



#%%キーボード待ち
def getkey(key):
    return(bool(ctypes.windll.user32.GetAsyncKeyState(key)&0x8000))
ESC = 0x1B          

#%%クリロー接離
class CLR():
    
    def __init__(self,com):
        self.com = com

    def press(self):
        word="FUS PRESS 290\r\n"
        self.com.write(word.encode())

    def separate(self):
        word="FUS SEPARATE 20\r\n"
        self.com.write(word.encode())        
        
#%%USBGPIO8
class GPIO8():

    def __init__(self,port):
        self.com = Serial(port=port,baudrate=57600,timeout=1)
    
    def set_high(self):
        word="gpio set 0 \r\n"
        self.com.write(word.encode())

    def set_low(self):
        word="gpio clear 0 \r\n"
        self.com.write(word.encode())
    
    def close(self):
        self.com.close()
    
#%%エンジンログを読む
class Engine():
    
    def __init__(self,port):
        self.com = Serial(port=port,baudrate=57600,timeout=1)
        self.clr = CLR(self.com)
        self.log = []
        self.modes = []

        #TMPコマンド開始
        self._tmp_command()

    #クリローを離間状態として初期化する
    def init_clr(self):
        #一旦当接してから離間する
        self.clr.press()
        time.sleep(2)
        self.clr.separate()

    #GPIO8をlowに初期化する
    def init_gpio8(self,port):
        self.gpio8 = GPIO8(port)
        self.gpio8.set_low()
                
    #エンジンから読んで
    def read(self):
        try:
            #print("kita")
            row = self._serial_read("utf-8")
            
            if "FusSepMot" in row:
                print(row)
            
            self.log.append(row)
            
            if "main / sub" in row:
                self.modes.append(self._return_mode(row))
        except:
            pass

    #クリローを当接する
    def press(self):
        self.clr.press()
        self.gpio8.set_high()

    #クリローを離間する       #
    def separate(self):
        self.clr.separate() 
        self.gpio8.set_low()        

    #comを閉じる
    def close(self):
        #tmpコマンド停止
        self._tmp_command()
        #通信着る        
        self.com.close()
        self.gpio8.close()
        #データ保存
        self._save()

    #温度ログ開始
    def _tmp_command(self):
        word="TMP\r\n"
        self.com.write(word.encode())

    #エンジンログから読む
    def _serial_read(self,coding):
        data = self.com.readline()
        data = data.strip().decode(coding) #先頭/末を消す
        return data
    
    #モード名を返す
    def _return_mode(self,row):
                
        tmp = row.split("=")
        tmp = tmp[1].split("/")
        num0 = int(tmp[0])
        num1 = int(tmp[1])        
        
        main_dict={0:"初期状態",1:"立上制御",2:"待機",3:"印刷",4:"停止",5:"省エネ"}
        sub_dict ={0:"初期状態",1:"プレ回転前",2:"プレ回転後",3:"リロード後",4:"待機モード",5:"印刷終了",6:"通紙後",7:"調整中",8:"通紙中",9:"ニップ測定",10:"全停止",11:"省エネ",}

        main = main_dict[num0]
        sub  = sub_dict [num1]

        return {"main":main, "sub":sub}

    #モード名を返す
    def _save(self):
        with open('output.txt','a') as f:
            for i in self.log:
                f.write(i+"\n")

#%%当接離間を判定する
def judge(modes):

    #1個以下のとき比較できないため、エラーを返す
    if len(modes)<2:
        return "err1"

    else:
        pre = modes[-2]
        aft = modes[-1]
        
        #前が
        if (pre["main"] == "待機") & (aft["main"] == "印刷"):
            return "press"

        if (pre["main"] == "印刷") & (aft["main"] == "待機"):
            return "separate"

        else:
            return "none"

#%%TMPリセット
def tmpreset(en):
    en._tmp_command()

#%%実行
engine = Engine(PORT1)
engine.init_clr()
engine.init_gpio8(PORT2)
print("initialized")

ts = time.time()

while True:
    
    #if time.time()-ts>20:
    #    break
    
    #ログを読む
    engine.read()
    
    #モードデータが更新される前に、判定とコマンドをやり続けてしまっている！！！！

    #判定する
    jdg = judge(engine.modes)


    #クリロを動かす
    if jdg == "press":
        engine.press()
    
    if jdg == "separate":
        engine.separate()
        
    if getkey(ESC) == True:
        break

print("loopend")

#終了処理
engine.close()