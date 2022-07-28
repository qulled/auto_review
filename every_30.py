import datetime as dt
import json
import os
import pickle
import time

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from data_for_bot import bot_alert_reviews, bot_alert_list_feed
from pars_feedback_table import get_article

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
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)


# options.add_argument('--headless')


def order_review(dict_article):
    for key in dict_article:
        article = dict_article.get(key)
        with open(f'up_feedbacks/list_reviews_opponent_{article}.json') as f:
            list_review = json.load(f)
        if len(list_review) == 0:
            bot_alert_list_feed(len(list_review))
            continue
        elif len(list_review) <= 10:
            bot_alert_reviews(len(list_review))
        else:
            count = ''
            check_hour = date.strftime("%H")
            if check_hour == '22' or check_hour == '23' or check_hour == '00' or check_hour == '01' or check_hour == '02' or check_hour == '03' or check_hour == '04' or check_hour == '05' or check_hour == '06':
                exit()
            else:
                try:
                    search_article_button = driver.find_element(By.XPATH,
                                                                '/html/body/div[1]/div/div/div[1]/div/div/div[1]/form/input')
                    search_article_button.send_keys(article)
                    time.sleep(1)
                    search_button = driver.find_element(By.CLASS_NAME, 'search__btn-search')
                    search_button.click()
                    time.sleep(1)
                    """проверка остатка отзывов на товаре"""
                    driver.refresh()
                    time.sleep(2)
                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")
                    get_feed = soup.find('button', class_='review__btn-new-review btn-')
                    for i in str(get_feed)[-15:]:
                        if i.isdigit():
                            count += i
                    if int(count) < 0:
                        bot_alert_reviews(int(count), article)
                        driver.quit()
                        exit()
                    elif int(count) <= 20:
                        bot_alert_reviews(int(count), article)
                    """заказ отзыва"""
                    get_review_button = driver.find_element(By.XPATH,
                                                            '/html/body/div[1]/div/div/div[1]/div/div/div[3]/ul/li/button')
                    get_review_button.click()
                    time.sleep(1)
                    pvz_button = driver.find_element(By.CLASS_NAME, 'vs__selected-options')
                    pvz_button.click()
                    take_old_pvz = driver.find_element(By.ID, 'vs1__option-0')
                    take_old_pvz.click()
                    time.sleep(3)
                    input_text_reviews = driver.find_element(By.TAG_NAME,
                                                             'textarea')
                    time.sleep(2)
                    input_text_reviews.click()
                    input_text_reviews.send_keys(list_review[0])
                    list_review.remove(list_review[0])
                    with open(f'up_feedbacks/list_reviews_opponent_{article}.json', 'w', encoding='UTF-8') as outfile:
                        json.dump(list_review, outfile)
                    send_review = driver.find_element(By.XPATH,
                                                      '/html/body/div[4]/div[1]/div/div/div/div/div/div/div[2]/div[8]/button[2]')
                    send_review.click()
                    time.sleep(5)
                except Exception as e:
                    driver.quit()
                    print('e:', e)
                finally:
                    search_article_button = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/div/div/div[1]/form/input')
                    search_article_button.click()
                    time.sleep(1)
                    search_article_button.send_keys(Keys.CONTROL,'a')
                    search_article_button.send_keys(Keys.BACKSPACE)

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
    dict_articles = get_article(table_id=SPREADSHEET_OPPONENT)
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
