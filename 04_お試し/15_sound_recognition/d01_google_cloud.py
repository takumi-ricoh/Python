# -*- coding: utf-8 -*-
"""
Spyderエディタ

これは一時的なスクリプトファイルです
"""

#coding:utf8
import base64
from googleapiclient import discovery
import httplib2
 
import pyaudio  #録音機能を使うためのライブラリ
import wave     #wavファイルを扱うためのライブラリ
 
#APIキーを設定
key = "YourAPIkey"
 
#音声を保存するファイル名
WAVE_OUTPUT_FILENAME = "sample10.wav"
 
#録音に関する基本情報
RECORD_SECONDS = 10 #録音する時間の長さ（秒）
iDeviceIndex = 0 #録音デバイスのインデックス番号
 
#APIのURL情報
DISCOVERY_URL = ('https://{api}.googleapis.com/$discovery/rest?'
                 'version={apiVersion}')
 
def record():
    #基本情報の設定
    FORMAT = pyaudio.paInt16 #音声のフォーマット
    CHANNELS = 1             #モノラル
    RATE = 44100             #サンプルレート
    CHUNK = 2**11            #データ点数
    audio = pyaudio.PyAudio()
 
    stream = audio.open(format=FORMAT, channels=CHANNELS,
            rate=RATE, input=True,
            input_device_index = iDeviceIndex, #録音デバイスのインデックス番号
            frames_per_buffer=CHUNK)
 
    #--------------録音開始---------------
 
    print ("recording...")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
 
 
    print ("finished recording")
 
    #--------------録音終了---------------
 
    stream.stop_stream()
    stream.close()
    audio.terminate()
 
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
 
 
 
#APIの情報を返す関数
def get_speech_service():
    http = httplib2.Http()
    return discovery.build(
        'speech', 'v1', http=http, discoveryServiceUrl=DISCOVERY_URL, developerKey=key)
 
def SpeechAPI():
    #音声ファイルを開く
    with open(WAVE_OUTPUT_FILENAME, 'rb') as speech:
        speech_content = base64.b64encode(speech.read()) 
 
    #APIの情報を取得して、音声認識を行う
    service = get_speech_service()
    service_request = service.speech().recognize(
        body={
            'config': {
                'encoding': 'LINEAR16',
                'sampleRateHertz': 44100,
                'languageCode': 'ja-JP', #日本語に設定
                'enableWordTimeOffsets': 'false',
            },
            'audio': {
                'content': speech_content.decode('UTF-8')
                }
            })
 
    #SpeechAPIによる認識結果を保存
    response = service_request.execute()
 
    #見やすいようにコンソール画面で出力
    for i in response["results"]:
        print(i["alternatives"][0]["transcript"],"confidence:" , i["alternatives"][0]["confidence"])
 
while True:
    record()
    SpeechAPI()