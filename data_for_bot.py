import requests
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
import datetime as dt
import logging
import os
import pickle
from logging.handlers import RotatingFileHandler
import time
import json
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


def parsing_info_for_bot_alert(url):
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument('--headless')
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    driver.get(url)
    cookies = pickle.load(open(f'cookies_mpboost.py', 'rb'))
    for cookie in cookies:
        driver.add_cookie(cookie)
    time.sleep(3)
    ransoms, reviews = '', ''
    dict_for_bot = {'Выкупы': '', 'Отзывы':''}
    try:
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        time.sleep(1)
        for card in soup.find_all('ul', class_="profile__stats stats"):
            if card.find_all('p', class_='stats__value'):
                quantity = card.find('p', class_='stats__value')
                quantity = quantity.get_text().strip()
                for i in quantity:
                    if i.isdigit():
                        ransoms += i
                    else:
                        dict_for_bot['Выкупы']= int(ransoms)
                        ransoms = ''
                        break
            if card.find_all('p', class_='stats__value')[1]:
                quantity = card.find_all('p', class_='stats__value')[1]
                quantity = quantity.get_text().strip()
                for i in quantity:
                    if i.isdigit():
                        ransoms += i
                    else:
                        dict_for_bot['Отзывы'] = int(ransoms)
                        ransoms = ''
                        break
    except Exception as e:
        print(e)
    finally:
        driver.quit()
        return dict_for_bot


def bot_alert(dict):
    print(dict.get('Отзывы'))
    if dict.get('Отзывы') < 10:
        with open('chat_id.json') as json_file:
            data = json.load(json_file)
            for chat_id in data:
                requests.get(f'https://api.telegram.org/bot5523517805:AAEtoirEqgvK0kiSCaG655pAbgVkfSC-dn4/sendMessage?chat_id={chat_id}&text=     !ВНИМАНИЕ! \n'
                             f'!!!Осталось отзывов - {dict.get("Отзывы")} шт.!!!')
    elif dict.get('Отзывы') < 50:
        with open('chat_id.json') as json_file:
            data = json.load(json_file)
            for chat_id in data:
                requests.get(f'https://api.telegram.org/bot5523517805:AAEtoirEqgvK0kiSCaG655pAbgVkfSC-dn4/sendMessage?chat_id={chat_id}&text=Осталось отзывов - {dict.get("Отзывы")} шт.!')
    if dict.get('Выкупы') < 10:
        with open('chat_id.json') as json_file:
            data = json.load(json_file)
            for chat_id in data:
                requests.get(
                    f'https://api.telegram.org/bot5523517805:AAEtoirEqgvK0kiSCaG655pAbgVkfSC-dn4/sendMessage?chat_id={chat_id}&text=     !ВНИМАНИЕ! \n'
                    f'!!!Осталось выкупов - {dict.get("Выкупы")} шт.!!!')
    elif dict.get('Выкупы') < 50:
        with open('chat_id.json') as json_file:
            data = json.load(json_file)
            for chat_id in data:
                requests.get(f'https://api.telegram.org/bot5523517805:AAEtoirEqgvK0kiSCaG655pAbgVkfSC-dn4/sendMessage?chat_id={chat_id}&text=Осталось выкупов - {dict.get("Выкупы")} шт.!')



def bot_alert_reviews(count,article,name,in_article):
    if count == 0:
        with open('chat_id.json') as json_file:
            data = json.load(json_file)
            for chat_id in data:
                requests.get(f'https://api.telegram.org/bot5523517805:AAEtoirEqgvK0kiSCaG655pAbgVkfSC-dn4/sendMessage?chat_id={chat_id}&text=     !ВНИМАНИЕ! \n'
                             f'!!!У товара: {article}, {name}, {in_article} закончился лимит отзывов! Невозможно оставить отзыв!!!')
    elif count < 20:
        with open('chat_id.json') as json_file:
            data = json.load(json_file)
            for chat_id in data:
                requests.get(f'https://api.telegram.org/bot5523517805:AAEtoirEqgvK0kiSCaG655pAbgVkfSC-dn4/sendMessage?chat_id={chat_id}&text='f'У товара: {article}, {name}, {in_article} лимит отзывов составляет {count} шт.!')


def bot_alert_list_feed(count):
    if count == 0:
        with open('chat_id.json') as json_file:
            data = json.load(json_file)
            for chat_id in data:
                requests.get(f'https://api.telegram.org/bot5523517805:AAEtoirEqgvK0kiSCaG655pAbgVkfSC-dn4/sendMessage?chat_id={chat_id}&text=     !ВНИМАНИЕ! \n'
                             f'!!!В таблице закончились отзывы, необходимо обновить таблицу!!!')
    elif count <= 30:
        with open('chat_id.json') as json_file:
            data = json.load(json_file)
            for chat_id in data:
                requests.get(f'https://api.telegram.org/bot5523517805:AAEtoirEqgvK0kiSCaG655pAbgVkfSC-dn4/sendMessage?chat_id={chat_id}&text='
                             f'В таблице осталось {count} отзывов!')



if __name__ == "__main__":
    date = dt.datetime.now()
    url = 'https://app.mpboost.pro/buyout'
    bot_alert(parsing_info_for_bot_alert(url))
