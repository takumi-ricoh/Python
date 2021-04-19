import requests
import json

#url
url = "https://api.gnavi.co.jp/RestSearchAPI/v3/"

#パラメータ：辞書で設定
params = {}
params["keyid"] = "xxxxxxxxxx"
params["freeword"] = "ハンバーグ"

#リクエスト結果
result_api1 = requests.get(url, params)
result_api2 = result_api1.json() #jsonに変換？

#リクエスト結果出力
count = len(result_api2['rest']) #レストラン情報
for count in range(count):
    print(result_api2['rest'][count]['address'])
    print(result_api2['rest'][count]['name'])
    print(result_api2['rest'][count]['code'])
    print(result_api2['rest'][count]['address']['areaname'])
    print(result_api2['rest'][count]['category'])
    print('-----------------------------')
