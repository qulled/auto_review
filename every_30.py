import datetime as dt
import os
import pickle
import random
import time

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager

# from data_for_bot import bot_alert_reviews, bot_alert_list_feed
from generator import get_article,get_phrase

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
load_dotenv('.env ')
SPREADSHEET_OPPONENT = os.getenv('SPREADSHEET_OPPONENT')
GH_TOKEN = os.getenv('GH_TOKEN')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
SPREADSHEET_ID_GENERATOR = os.getenv('SPREADSHEET_ID_GENERATOR')


def order_review(dict_article):
    count = ''
    for article in article_dict:
        article_name = dict_article.get(article)
        check_hour = date.strftime("%H")
        if check_hour == '22' or check_hour == '23' or check_hour == '00' or check_hour == '01' or check_hour == '02' or check_hour == '03' or check_hour == '04' or check_hour == '05' or check_hour == '06':
            exit()
        else:
            try:
                driver.get(f'https://app.mpboost.pro/reviews?search={article}')
                """проверка остатка отзывов на товаре"""
                driver.refresh()
                time.sleep(2)
                driver.execute_script('arguments[0].click();', WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div[3]/ul/li/button'))))
                print('начали заказ')
                time.sleep(3)
                try:
                    chose_size_button = driver.find_element(By.CLASS_NAME,'v-dropdown-menu__trigger')
                    chose_size_button.click()
                    print('меню размера')
                    time.sleep(1)
                    size_button = driver.find_elements(By.CLASS_NAME,'option__btn')
                    click_size_button = size_button[random.randint(0,len(size_button)-1)]
                    click_size_button.click()
                    print('выбрали размер')
                    time.sleep(1)
                except:
                    print('нет размеров')
                    pass
                pvz_button = driver.find_element(By.CLASS_NAME, 'vs__selected-options')
                pvz_button.click()
                take_old_pvz = driver.find_element(By.ID, 'vs1__option-0')
                take_old_pvz.click()
                time.sleep(1)
                print('выбрали ПВЗ')
                input_text_reviews = driver.find_elements(By.TAG_NAME,'textarea')
                time.sleep(1)
                input_text_reviews[0].click()
                time.sleep(1)
                #driver.execute_script("arguments[0].innerHTML = '{}'".format(list_review[0]), input_text_reviews[0])
                input_text_reviews[0].send_keys(get_phrase(table_id_generator,article,article_name))
                time.sleep(5)
                print('встввили отзыв')
                send_review_button = driver.find_element(By.CSS_SELECTOR,'.controls__btn-replenish')
                send_review_button.click()
                print('окончили заказ, отправили отзыв')
            except Exception as e:
                print('e:', e)
    return


def auth(url):
    driver.get(url)
    cookies = pickle.load(open(f'cookies_mpboost.py', 'rb'))
    for cookie in cookies:
        driver.add_cookie(cookie)
    time.sleep(5)
    return '+'


if __name__ == "__main__":
    table_id = SPREADSHEET_ID
    table_id_generator = SPREADSHEET_ID_GENERATOR
    date = dt.datetime.now()
    url = 'https://app.mpboost.pro/reviews'
    article_dict = get_article(table_id_generator)
    try:
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--headless")
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()),options=options)
        driver.maximize_window()
        if auth(url) == '+':
            order_review(article_dict,)
    except Exception as e:
        print(e)
    finally:
        driver.quit()
