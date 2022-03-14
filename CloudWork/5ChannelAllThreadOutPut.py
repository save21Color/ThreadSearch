from bs4 import BeautifulSoup
import requests
import os,sys
import json
import re
import csv
import codecs

def AllThreadLoad():
    url = input("該当するスレッドのURLを入力してください: ")
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    #html取得
    soup = BeautifulSoup(response.text,'html.parser')
    #タイトルの取得
    title = soup.find(class_="title")
    #全レスを格納しているpostタブを取得
    post = soup.find_all(class_="post")
    result = {}
    result["title"] = title.text
    result["content"] = []
    for res in post:
        tag = res.contents[0]
        content = res.contents[1].text
        data = JsonLoad(tag,content)
        result["content"].append(data)
    # Jsonファイル生成
    f = open("AllThread.json","w")
    # インデント、エンコードしつつJsonに出力
    json.dump(result,f,ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    print("complete!")
    print(result)

# Json形式のデータをロードする
def JsonLoad(tag,content):
    resData = {}
    text = content
    # スレッドID,名前,時刻,ユーザーIDを格納する
    threadid = tag.contents[0].text
    name = tag.contents[1].text
    time = tag.contents[2].text
    userid = tag.contents[3].text.strip("ID:")
    resData = {"threadid":threadid,"name":name,"time":time,"userid":userid,"text":text}
    return resData

if __name__ == '__main__':
    AllThreadLoad()