# -*- coding: utf-8 -*-

from selenium import webdriver
import time
import socket


def auto():
    opt = webdriver.ChromeOptions()
    opt.add_argument('--headless')
    opt.binary_location = '/app/.apt/usr/bin/google-chrome'  # Heroku �ł̓o�C�i�����w�肷��
    driver_path = '/app/.chromedriver/bin/chromedriver'  # Heroku �ɂ����� driver �̈ʒu
    driver = webdriver.Chrome(executable_path=driver_path, chrome_options=opt)

    driver.get('https://www.youtube.com/watch?v=s1sHeQnPu90')

    time.sleep(15)


def get_ip():
    host = socket.gethostname()
    print(host)

    ip = socket.gethostbyname(host)
    print(ip)


if __name__ == '__main__':
    auto()
    get_ip()
