# -*- coding: utf-8 -*-

# PyDrive での対象ファイルは Root > PythonWorks > Git > WeatherExtractor
# PyDrive での対象ファイルは Root > PythonWorks > ' Result Stock > AutoYouTubeResult.csv

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from selenium import webdriver
import time
import socket

import re
from bs4 import BeautifulSoup
import urllib.request as req

import datetime
import csv


def auth_google():
    # Google Oauth 認証を行う
    gauth = GoogleAuth()

    gauth.LoadCredentialsFile('credentials.json')
    if gauth.credentials is None:
        # Authenticate if they're not there
        # gauth.LocalWebserverAuth()
        gauth.CommandLineAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile('credentials.json')

    drive = GoogleDrive(gauth)

    # YouTubeAutoResult.csv を操作してみる
    # 操作したいファイルがあるフォルダの URL から、ID を取得する
    # 例: https://drive.google.com/drive/u/0/folders/16k1-Ok7OHFjSPtMkvuVEoBmLUBqlKH9i
    drive_folder_id = '16k1-Ok7OHFjSPtMkvuVEoBmLUBqlKH9i'
    query = '"{0}" in parents and trashed=false'.format(drive_folder_id)
    # 指定のフォルダ内のファイル一覧を ID と共に取得する
    file_list = drive.ListFile({'q': query}).GetList()
    for file in file_list:
        if file['title'] == 'YouTubeAutoResult.csv':  # YouTubeAutoResult.csv を取得してダウンロードする
            content = file.GetContentString()
            file2 = file
            break
        else:
            pass

    file2.GetContentFile('a.csv')  # csv ファイルとしてダウンロード
    file2.Trash()  # WeatherResult.csv をゴミ箱に移動
    file2.UnTrash()  # ゴミ箱の外に移動?
    file2.Delete()  # Hard Delete

    return drive


def auto():
    opt = webdriver.ChromeOptions()
    opt.add_argument('--headless')
    opt.binary_location = '/app/.apt/usr/bin/google-chrome'  # Heroku ではバイナリを指定する
    driver_path = '/app/.chromedriver/bin/chromedriver'  # Heroku における driver の位置
    # driver = webdriver.Chrome('../chromedriver-73.exe', options=opt)
    driver = webdriver.Chrome(executable_path=driver_path, chrome_options=opt)

    """
    driver = webdriver.Chrome('../chromedriver-73.exe')
    """

    driver.get('https://www.youtube.com/watch?v=s1sHeQnPu90')

    time.sleep(15)


# YouTube の動画ページにアクセスして 視聴回数を抜き出す
# 本当は上の auto 関数から視聴回数を抜き出した方が効率がいいけど、追記するのがめんどくさかったのでこちらでやった
def youtube_search():
    url = 'https://www.youtube.com/watch?v=s1sHeQnPu90'

    # urlopen() でデータを取得
    res = req.urlopen(url)

    # BeautifulSoup オブジェクトの作成
    soup = BeautifulSoup(res, "html.parser")

    # 任意のデータを抽出
    # views = soup.select('#count')
    # views = soup.select('span.view-count style-scope yt-view-count-renderer')
    views_content = soup.select_one('div.watch-view-count')

    # print(views.string)
    # print(soup)

    pattern = '([0-9.]*)' + ' ' + '([回視聴]*)'
    a = re.search(pattern, views_content.string)
    views = a.group(1)
    print(views)
    return views


def get_ip():
    host = socket.gethostname()
    print(host)

    ip = socket.gethostbyname(host)
    print(ip)
    return host, ip


# csv に書き込み
def write_csv(views, host, ip):
    # 現在の時間を取得
    dt_now = datetime.datetime.now()
    td_9h = datetime.timedelta(hours=9)
    dt_now_japan = dt_now + td_9h
    year = dt_now_japan.year
    month = dt_now_japan.month
    day = dt_now_japan.day
    present_time = dt_now_japan.time()

    with open('a.csv', mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([year, month, day, present_time, host, ip, views])


def upload_file(drive):
    # PythonWorks > ' Result Stock のフォルダ ID
    file2 = drive.CreateFile({'parents': [{'id': '16k1-Ok7OHFjSPtMkvuVEoBmLUBqlKH9i'}]})
    file2.SetContentFile('a.csv')
    file2['title'] = 'YouTubeAutoResult.csv'
    file2.Upload()


if __name__ == '__main__':
    drive = auth_google()

    auto()
    views = youtube_search()
    ip_tuple = get_ip()
    write_csv(views=views, host=ip_tuple[0], ip=ip_tuple[1])

    upload_file(drive=drive)
