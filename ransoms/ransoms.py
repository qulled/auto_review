from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import datetime as dt
import logging
import os
import pickle
from logging.handlers import RotatingFileHandler
import time

options = Options()

prefs = {'download.default_directory': r'C:\Users\ikaty\PycharmProjects\parser_margin\excel_docs'}

options.add_experimental_option('prefs', prefs)
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--headless')

driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.execute_cdp_cmd('Network.setUserAgentOverride', {
    "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36'})


def auth(url):
    driver.get(url)
    cookies = pickle.load(open(f'cookies_mpboost.py', 'rb'))
    for cookie in cookies:
        driver.add_cookie(cookie)
    time.sleep(3)
    return parsing_page()


def parsing_page():
    dict_rans = {}
    ransoms = ''
    try:
        all_ransoms_button = driver.find_element(By.CLASS_NAME, 'filters__btn')
        all_ransoms_button.click()
        time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        time.sleep(1)
        for card in soup.find_all('li', class_="buyouts__buyout buyout"):
            if card.find_all('p', class_='product__id'):
                article = card.find('p', class_='product__id')
                article = article.get_text().strip()
                article = article[-8:]
            if card.find_all('p', class_='stats__value'):
                rans = card.find_all('p', class_='stats__value')[1]
                rans = rans.get_text().strip()
                for i in rans:
                    if i.isdigit():
                        ransoms += i
                    else:
                        break
            if card.find_all('p', class_="info__date"):
                date_text = card.find('p', class_='info__date')
                date_text = date_text.get_text().strip()
                date_text = date_text[:-6]
                if date_text == f'{day} {month_name}' and card.find('span',
                                                                    class_='status__completed').get_text().strip() == 'Завершен':
                    dict_rans[article] = int(ransoms)
                    ransoms = ''

    except Exception as e:
        print(e)
    finally:
        driver.quit()
        return print(dict_rans)


if __name__ == "__main__":
    date = dt.datetime.now() - dt.timedelta(days=1)
    day = date.strftime('%d')
    month = date.strftime('%m')
    month_dict = {'01': 'января', '02': 'февраля', '03': 'марта', '04': 'апреля', '05': 'мая', '06': 'июня',
                  '07': 'июля', '08': 'августа', '09': 'сентября', '10': 'октября', '11': 'ноября', '12': 'декабря'}
    month_name = month_dict.get(f'{month}')
    # print(f'{day} {month_name}')
    url = 'https://app.mpboost.pro/buyout'
    auth(url)
