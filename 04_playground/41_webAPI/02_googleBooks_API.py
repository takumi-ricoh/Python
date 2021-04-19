import requests
import json

#ベースurl
base_url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:'

#ISBN
ISBN = "978-4-03-237110-9"
isbn = ISBN.replace("-","") #-の削除

#URL
url = base_url + isbn

#パラメータ：辞書で設定
#params = {}

#リクエスト結果
result_api1 = requests.get(url)
result_api2 = result_api1.json() #jsonに変換？
result_api3 = result_api1.text

print(result_api3)