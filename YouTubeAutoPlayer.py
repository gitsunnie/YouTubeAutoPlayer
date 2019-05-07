# -*- coding: utf-8 -*-

from selenium import webdriver
import time
import socket

import re
from bs4 import BeautifulSoup
import urllib.request as req

import datetime
import csv


def auto():
    # opt = webdriver.ChromeOptions()
    # opt.add_argument('--headless')
    # opt.binary_location = '/app/.apt/usr/bin/google-chrome'  # Heroku ではバイナリを指定する
    # driver_path = '/app/.chromedriver/bin/chromedriver'  # Heroku における driver の位置
    # driver = webdriver.Chrome('../chromedriver-73.exe', options=opt)
    driver = webdriver.Chrome('../chromedriver-73.exe')

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


def write_csv(views, host, ip):
    # 現在の時間を取得
    dt_now = datetime.datetime.now()
    year = dt_now.year
    month = dt_now.month
    day = dt_now.day
    present_time = dt_now.time()

    with open('YouTubeResult.csv', mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([year, month, day, present_time, host, ip, views])


if __name__ == '__main__':
    auto()
    views = youtube_search()
    ip_tuple = get_ip()
    write_csv(views=views, host=ip_tuple[0], ip=ip_tuple[1])
