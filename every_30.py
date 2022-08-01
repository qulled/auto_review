import datetime as dt
import json
import os
import pickle
import random
import time

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from data_for_bot import bot_alert_reviews, bot_alert_list_feed
from pars_feedback_table import get_article,final_dict

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
load_dotenv('.env ')
SPREADSHEET_OPPONENT = os.getenv('SPREADSHEET_OPPONENT')

options = Options()

prefs = {'download.default_directory': r'C:\Users\ikaty\PycharmProjects\parser_margin\excel_docs'}

options.add_experimental_option('prefs', prefs)
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)


options.add_argument('--headless')


def order_review(dict_article):
    count = ''
    for key_word in dict_article:
        article = key_word
        name = dict_article.get(key_word)[0]
        in_article = dict_article.get(key_word)[1]
        check = dict_article.get(key_word)[3]
        if check == '+':
            with open(f'up_feedbacks/list_reviews_opponent_{article}.json',encoding='UTF-8') as f:
                list_review = json.load(f)
            if len(list_review) == 0:
                bot_alert_list_feed(len(list_review))
                continue
            elif len(list_review) <= 10:
                bot_alert_reviews(len(list_review))
            else:
                check_hour = date.strftime("%H")
                if check_hour == '22' or check_hour == '23' or check_hour == '00' or check_hour == '01' or check_hour == '02' or check_hour == '03' or check_hour == '04' or check_hour == '05' or check_hour == '06':
                    exit()
                else:
                    try:
                        # search_article_button = driver.find_element(By.TAG_NAME,'input')
                        # search_article_button.send_keys(article)
                        # time.sleep(2)
                        # search_button = driver.find_element(By.CLASS_NAME, 'search__btn-search')
                        # search_button.click()
                        # time.sleep(2)
                        print(f'https://app.mpboost.pro/reviews?search={article}')
                        driver.get(f'https://app.mpboost.pro/reviews?search={article}')
                        """проверка остатка отзывов на товаре"""
                        driver.refresh()
                        time.sleep(2)
                        html = driver.page_source
                        soup = BeautifulSoup(html, "html.parser")
                        get_feed = soup.find('button', class_='review__btn-new-review btn-')
                        for i in str(get_feed)[-15:]:
                            if i.isdigit():
                                count += i
                        if int(count) <= 20:
                            bot_alert_reviews(int(count), article, name, in_article)
                        """заказ отзыва"""
                        driver.execute_script('arguments[0].click();', WebDriverWait(driver, 20).until(
                            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div[3]/ul/li/button'))))
                        print('начали заказ')
                        time.sleep(2)
                        chose_size_button = driver.find_element(By.CLASS_NAME,'v-dropdown-menu__trigger')
                        chose_size_button.click()
                        print('меню размера')
                        time.sleep(1)
                        size_button = driver.find_elements(By.CLASS_NAME,'option__btn')
                        click_size_button = size_button[random.randint(0,len(size_button)-1)]
                        click_size_button.click()
                        print('выбрали размер')
                        time.sleep(1)
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
                        # driver.execute_script("arguments[0].innerHTML = '{}'".format(list_review[0]), input_text_reviews[0])
                        # time.sleep(5)
                        input_text_reviews[0].send_keys(list_review[0])
                        print('встввили отзыв')
                        list_review.remove(list_review[0])
                        with open(f'up_feedbacks/list_reviews_opponent_{article}.json', 'w', encoding='UTF-8') as outfile:
                            json.dump(list_review, outfile)
                        driver.execute_script('arguments[0].click();', WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, '/html/body/div[4]/div[1]/div/div/div/div/div/div/div[2]/div[8]/button[2]'))))
                        print('окончили заказ, отправили отзыв')
                        # close_but = driver.find_element(By.XPATH,'/html/body/div[4]/div[1]/div/div/div/div/button')
                        # close_but.click()
                        time.sleep(2)
                    except Exception as e:
                        driver.quit()
                        print('e:', e)
                    # finally:
                    #     search_article_button = driver.find_element(By.TAG_NAME,'input')
                    #     search_article_button.click()
                    #     time.sleep(1)
                    #     search_article_button.send_keys(Keys.CONTROL,'a')
                    #     search_article_button.send_keys(Keys.BACKSPACE)
        elif check == '-':
                count = '0'
                bot_alert_reviews(int(count), article, name, in_article)
                dict_article.get(key_word)[3] = '1'
                with open(f'up_feedbacks/check_article.json', 'w', encoding='UTF-8') as outfile:
                    json.dump(dict_article, outfile)
                continue
    return


def auth(url):
    driver.get(url)
    cookies = pickle.load(open(f'cookies_mpboost.py', 'rb'))
    for cookie in cookies:
        driver.add_cookie(cookie)
    time.sleep(5)
    return '+'


if __name__ == "__main__":
    date = dt.datetime.now()
    url = 'https://app.mpboost.pro/reviews'
    final_dict(url)
    with open('up_feedbacks/check_article.json') as f:
        dict_articles = json.load(f)
    if len(dict_articles) > 0:
        try:
            driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36'})
            if auth(url) == '+':
                order_review(dict_articles)
        except Exception as e:
            print(e)
        finally:
            driver.quit()
    driver.quit()
