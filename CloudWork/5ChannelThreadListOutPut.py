from bs4 import BeautifulSoup
import requests
import os,sys
import json
import re
import csv
import codecs

def ChannelThreadListLoad():
    url = input("該当するURLを入力してください: ")
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    # Htmlを取得
    soup = BeautifulSoup(response.text,'html.parser')
    # このページのベースルーティングを取得
    base = soup.find('base')
    # 末尾URL取得
    a = json.dumps(base.attrs)
    s = json.loads(a)
    baseUrl = re.findall('.*?/',url)[0]+ re.findall('.*?/',url)[1] + re.findall('.*?/',url)[2] + s["href"]
    # 全リンクを格納しているtradを取得
    trad = soup.find(id="trad")
    allLink = trad.find_all('a')
    # カレントディレクトリにcsvファイル生成
    c = open('./5ChannelThreadList.csv','w',newline='')
    writer = csv.writer(c)
    # ヘッダを設定
    headders = ['id','title','count','url']
    writer.writerow(headders)
    # 1行ずつ処理
    for link in allLink:
        CsvWriter(link,baseUrl,writer)
    print("Complete!")
    c.close()

# スレッド一覧のスレッド情報を一行ずつCSVに書き出す
def CsvWriter(link,baseUrl,writer):
    # 末尾URLを取得
    dump = json.dumps(link.attrs)
    result = json.loads(dump)
    url = baseUrl + result["href"]
    # 「:」でsplitしてid欄を取得
    id = link.text.split(':')[0]
    cnt = len(link.text.split(':'))
    # 正規表現で「括弧に囲まれた0~9で表現された数値」を検索、取得する。
    count = re.search(r'(\()([0-9]*?)\)', link.text.split(':')[cnt-1])[0].strip('()')
    # タイトル取得
    title = link.text.strip(id+':').strip('('+count+')').replace('\xa9','')
    # 1行書き込み
    writeList  = [id,title,count,url]
    writer.writerow(writeList)
    print(link)

if __name__ == "__main__":
    ChannelThreadListLoad()
