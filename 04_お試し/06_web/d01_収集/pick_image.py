# -*- coding: utf-8 -*-
"""
Created on Wed May 18 10:10:30 2016

@author: p000495138
"""

"""
使い方：
１．collection_url.txtは消しておく
２．実行
★URLによってはうまくダウンロードできない場合もある
"""

#追加！：　requestをurllibから
import urllib.request as urllib2
import urllib
import os.path
import sys
from html.parser import HTMLParser as HTMLParser


"""ダウンロードする関数"""
def download(url):
    img = urllib2.urlopen(url)
    print(img)
    print(os.path.basename(url))
    localfile = open(os.path.basename(url), 'wb')
    localfile.write(img.read())
    img.close()
    localfile.close()

"""画像ファイルのルートパス(url)を調べる関数"""
def get_url_root(url):
    if("http://" in url):
        url_delet_http = url.lstrip("http://")
        if("/" in url_delet_http):
            url_root = "http://" + url_delet_http[0:url_delet_http.find("/")]
            return url_root
    elif("https://" in url):
        url_delet_http = url.lstrip("https://")
        if("/" in url_delet_http):
            url_root = "http://" + url_delet_http[0:url_delet_http.find("/")]
            return url_root
    return 0

"""画像のURLのみを調べる関数"""
class imgParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)

    def handle_starttag(self,tagname,attribute):
        if tagname.lower() == "img":
            for i in attribute:
                if i[0].lower() == "src":
                    img_url=i[1]
                    # 取得した写真のURLを集めたファイルの作成
                    f = open("collection_url.txt","a")
                    f.write("%s\t"%img_url)
                    f.close()

"""メインルーチン"""
if __name__ == "__main__":

    #urlの取得
    print('写真を取得したいサイトのURLを入力してください。')
    input_url = input('>>>  ')
    serch_url = input_url
    
    #htmlデータを取得
    htmldata = urllib2.urlopen(serch_url)

    print('現在画像ファイルを取得中です...')

    #画像のURLを取得しテキストファイル(collection_url)に保存
    parser = imgParser() #コンストラクタ
    temp = htmldata.read()
    temp2 =temp.decode('utf-8')
    parser.feed(temp2)
    parser.close()
    htmldata.close()

    #生成したファイルの読み込んでリスト化
    f = open("collection_url.txt","r")
    for row in f:
        row_url = row.split('\t')
        len_url = len(row_url)
    f.close()

    #画像URLの最終行を除去
    number_url = []
    for i in range(0,(len_url-1)):
        number_url.append(row_url[i])

    #画像のダウンロード(download関数を使用)
    for j in range(0,(len_url-1)):
        url = number_url[j]
        print (url)
        if("../" in url):
            root_url = get_url_root(serch_url)
            if(root_url!=0):
                url2 = url.replace("..",root_url)
                print(url,url2)
                download(url2)
        elif("http://" in url):
            download(url)
        elif("https://" in url):
            download(url)
        else:
            pass
#            download(input_url + url)

    print('画像のダウンロードが終了しました。')

    # ファイルの削除
    os.remove("collection_url.txt")