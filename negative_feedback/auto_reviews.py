from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import datetime as dt
import logging
import json
import pickle
import random
from logging.handlers import RotatingFileHandler
import time
from parser_negative_reviews import get_feedback, search_rootId
from data_for_bot import bot_alert_reviews, bot_alert_list_feed

options = Options()

prefs = {'download.default_directory': r'C:\Users\ikaty\PycharmProjects\parser_margin\excel_docs'}

options.add_experimental_option('prefs', prefs)
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
# options.add_argument('--headless')



def order_review(article, key, list_review):
    day1, day2, day3 = date.strftime('%d'), date.strftime('%d'), date.strftime('%d')
    count = ''
    add_new_time_1 = random.randint(10, 20)
    add_new_time_2 = random.randint(45, 60)
    add_new_time_3 = random.randint(75, 90)
    review_1_hour = (date + dt.timedelta(minutes=add_new_time_1)).strftime("%H")
    review_1_minute = (date + dt.timedelta(minutes=add_new_time_1)).strftime("%M")
    review_2_hour = (date + dt.timedelta(minutes=add_new_time_2)).strftime("%H")
    review_2_minute = (date + dt.timedelta(minutes=add_new_time_2)).strftime("%M")
    review_3_hour = (date + dt.timedelta(minutes=add_new_time_3)).strftime("%H")
    review_3_minute = (date + dt.timedelta(minutes=add_new_time_3)).strftime("%M")
    if review_1_hour == '23' or review_1_hour == '00' or review_1_hour == '01' or review_1_hour == '02' or review_1_hour == '03' or review_1_hour == '04' or review_1_hour == '05' or review_1_hour == '06':
        review_1_hour = '07'
        review_1_minute = random.randint(1, 25)
        if review_1_hour == '23':
            day1 = (date + dt.timedelta(hours=5)).strftime('%d')
    elif review_1_hour == '22' and int(review_1_minute) >= 30:
        day1 = (date + dt.timedelta(hours=5)).strftime('%d')
        review_1_hour = '07'
        review_1_minute = random.randint(1, 25)
    if review_2_hour == '22' or review_2_hour == '23' or review_2_hour == '00' or review_2_hour == '01' or review_2_hour == '02' or review_2_hour == '03' or review_2_hour == '04' or review_2_hour == '05' or review_2_hour == '06':
        if review_2_hour == '22' or review_2_hour == '23' or review_2_hour == '00':
            day2 = (date + dt.timedelta(hours=5)).strftime('%d')
        review_2_hour = '07'
        review_2_minute = random.randint(40, 59)
    if review_3_hour == '22' or review_3_hour == '23' or review_3_hour == '00' or review_3_hour == '01' or review_3_hour == '02' or review_3_hour == '03' or review_3_hour == '04' or review_3_hour == '05' or review_3_hour == '06':
        if review_3_hour == '22' or review_3_hour == '23' or review_3_hour == '00':
            day3 = (date + dt.timedelta(hours=5)).strftime('%d')
        review_3_hour = '08'
        review_3_minute = random.randint(15, 35)
    try:
        search_article_button = driver.find_element(By.XPATH,
                                                    '/html/body/div[1]/div/div/div[1]/div/div/div[1]/form/input')
        search_article_button.send_keys(article)
        time.sleep(1)
        search_button = driver.find_element(By.CLASS_NAME, 'search__btn-search')
        search_button.click()
        time.sleep(1)
        """ПЕРВЫЙ ОТЗЫВ"""
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        get_feed = soup.find('button', class_ = 'review__btn-new-review btn-')
        for i in str(get_feed)[-15:]:
            if i.isdigit():
                count += i
        if int(count) < 0:
            bot_alert_reviews(int(count), article)
            driver.quit()
            exit()
        elif int(count) <= 20:
            bot_alert_reviews(int(count), article)
        get_review_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div[3]/ul/li/button')
        get_review_button.click()
        time.sleep(1)
        pvz_button = driver.find_element(By.CLASS_NAME,'vs__selected-options')
        pvz_button.click()
        take_old_pvz = driver.find_element(By.ID, 'vs1__option-0')
        take_old_pvz.click()
        time.sleep(3)
        calendar = driver.find_element(By.CLASS_NAME,
                                               f'btn-calendar__label')
        calendar.click()
        time.sleep(1)
        day_button = driver.find_element(By.XPATH,
                                         '/html/body/div[5]/div[1]/div/div/div/div/div/div/div[1]/div/div/div[7]/input')
        day_button.send_keys(Keys.BACKSPACE)
        day_button.send_keys(Keys.BACKSPACE)
        time.sleep(1)
        day_button.send_keys(day1)
        day_button.send_keys(Keys.ENTER)
        time.sleep(1)
        # month_button = driver.find_element(By.XPATH,
        #                                  '/html/body/div[5]/div[1]/div/div/div/div/div/div/div[1]/div/div/div[8]/input')
        # year_button = driver.find_element(By.XPATH,
        #                                    '/html/body/div[5]/div[1]/div/div/div/div/div/div/div[1]/div/div/div[9]/input')
        hour_button = driver.find_element(By.XPATH,'/html/body/div[5]/div[1]/div/div/div/div/div/div/div[2]/div/div/div[5]/input')
        hour_button.click()
        hour_button.send_keys(Keys.DELETE)
        hour_button.send_keys(Keys.BACKSPACE)
        hour_button.send_keys(review_1_hour)
        hour_button.send_keys(Keys.ENTER)
        time.sleep(1)
        minute_button = driver.find_element(By.XPATH,'/html/body/div[5]/div[1]/div/div/div/div/div/div/div[2]/div/div/div[6]/input')
        minute_button.click()
        minute_button.send_keys(Keys.DELETE)
        minute_button.send_keys(Keys.BACKSPACE)
        minute_button.send_keys(review_1_minute)
        hour_button.send_keys(Keys.ENTER)
        save_calendar_button = driver.find_element(By.XPATH,'/html/body/div[5]/div[1]/div/div/div/div/button[1]')
        save_calendar_button.click()
        time.sleep(1)
        input_text_reviews = driver.find_element(By.XPATH,'/html/body/div[4]/div[1]/div/div/div/div/div/div/div[2]/div[5]/textarea')
        input_text_reviews.click()
        input_text_reviews.send_keys(list_review[0])
        time.sleep(500)
        list_review.remove(list_review[0])
        with open('for_negative_list_reviews.json', 'w', encoding='UTF-8') as outfile:
            json.dump(list_review, outfile)
        send_review = driver.find_element(By.XPATH,'/html/body/div[4]/div[1]/div/div/div/div/div/div/div[2]/div[8]/button[2]')
        send_review.click()
        time.sleep(10)

        """ВТОРОЙ ОТЗЫВ"""
        driver.refresh()
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        time.sleep(5)
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
        get_review_button = driver.find_element(By.XPATH,
                                                '/html/body/div[1]/div/div/div[1]/div/div/div[3]/ul/li/button')
        get_review_button.click()
        time.sleep(1)
        pvz_button = driver.find_element(By.CLASS_NAME, 'vs__selected-options')
        pvz_button.click()
        take_old_pvz = driver.find_element(By.ID, 'vs1__option-0')
        take_old_pvz.click()
        time.sleep(3)
        calendar = driver.find_element(By.CLASS_NAME,
                                       f'btn-calendar__label')
        calendar.click()
        time.sleep(1)
        day_button = driver.find_element(By.XPATH,
                                         '/html/body/div[5]/div[1]/div/div/div/div/div/div/div[1]/div/div/div[7]/input')
        day_button.send_keys(Keys.BACKSPACE)
        day_button.send_keys(Keys.BACKSPACE)
        time.sleep(1)
        day_button.send_keys(day2)
        day_button.send_keys(Keys.ENTER)
        time.sleep(1)
        # month_button = driver.find_element(By.XPATH,
        #                                  '/html/body/div[5]/div[1]/div/div/div/div/div/div/div[1]/div/div/div[8]/input')
        # year_button = driver.find_element(By.XPATH,
        #                                    '/html/body/div[5]/div[1]/div/div/div/div/div/div/div[1]/div/div/div[9]/input')
        hour_button = driver.find_element(By.XPATH,
                                          '/html/body/div[5]/div[1]/div/div/div/div/div/div/div[2]/div/div/div[5]/input')
        hour_button.click()
        hour_button.send_keys(Keys.DELETE)
        hour_button.send_keys(Keys.BACKSPACE)
        hour_button.send_keys(review_2_hour)
        hour_button.send_keys(Keys.ENTER)
        time.sleep(1)
        minute_button = driver.find_element(By.XPATH,
                                            '/html/body/div[5]/div[1]/div/div/div/div/div/div/div[2]/div/div/div[6]/input')
        minute_button.click()
        minute_button.send_keys(Keys.DELETE)
        minute_button.send_keys(Keys.BACKSPACE)
        minute_button.send_keys(review_2_minute)
        hour_button.send_keys(Keys.ENTER)
        save_calendar_button = driver.find_element(By.XPATH, '/html/body/div[5]/div[1]/div/div/div/div/button[1]')
        save_calendar_button.click()
        time.sleep(1)
        input_text_reviews = driver.find_element(By.XPATH,
                                                 '/html/body/div[4]/div[1]/div/div/div/div/div/div/div[2]/div[5]/textarea')
        input_text_reviews.click()
        input_text_reviews.send_keys(list_review[0])
        list_review.remove(list_review[0])
        with open('for_negative_list_reviews.json', 'w', encoding='UTF-8') as outfile:
            json.dump(list_review, outfile)
        send_review = driver.find_element(By.XPATH,
                                          '/html/body/div[4]/div[1]/div/div/div/div/div/div/div[2]/div[8]/button[2]')
        send_review.click()
        time.sleep(10)
        """ТРЕТИЙ ОТЗЫВ"""
        driver.refresh()
        time.sleep(5)
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
        get_review_button = driver.find_element(By.XPATH,
                                                '/html/body/div[1]/div/div/div[1]/div/div/div[3]/ul/li/button')
        get_review_button.click()
        time.sleep(1)
        pvz_button = driver.find_element(By.CLASS_NAME, 'vs__selected-options')
        pvz_button.click()
        take_old_pvz = driver.find_element(By.ID, 'vs1__option-0')
        take_old_pvz.click()
        time.sleep(3)
        calendar = driver.find_element(By.CLASS_NAME,
                                       f'btn-calendar__label')
        calendar.click()
        time.sleep(1)
        day_button = driver.find_element(By.XPATH,
                                         '/html/body/div[5]/div[1]/div/div/div/div/div/div/div[1]/div/div/div[7]/input')
        day_button = driver.find_element(By.XPATH,
                                         '/html/body/div[5]/div[1]/div/div/div/div/div/div/div[1]/div/div/div[7]/input')
        day_button.send_keys(Keys.BACKSPACE)
        day_button.send_keys(Keys.BACKSPACE)
        time.sleep(1)
        day_button.send_keys(day3)
        day_button.send_keys(Keys.ENTER)
        time.sleep(1)
        # month_button = driver.find_element(By.XPATH,
        #                                  '/html/body/div[5]/div[1]/div/div/div/div/div/div/div[1]/div/div/div[8]/input')
        # year_button = driver.find_element(By.XPATH,
        #                                    '/html/body/div[5]/div[1]/div/div/div/div/div/div/div[1]/div/div/div[9]/input')
        hour_button = driver.find_element(By.XPATH,
                                          '/html/body/div[5]/div[1]/div/div/div/div/div/div/div[2]/div/div/div[5]/input')
        hour_button.click()
        hour_button.send_keys(Keys.DELETE)
        hour_button.send_keys(Keys.BACKSPACE)
        hour_button.send_keys(review_3_hour)
        hour_button.send_keys(Keys.ENTER)
        time.sleep(1)
        minute_button = driver.find_element(By.XPATH,
                                            '/html/body/div[5]/div[1]/div/div/div/div/div/div/div[2]/div/div/div[6]/input')
        minute_button.click()
        minute_button.send_keys(Keys.DELETE)
        minute_button.send_keys(Keys.BACKSPACE)
        minute_button.send_keys(review_3_minute)
        hour_button.send_keys(Keys.ENTER)
        save_calendar_button = driver.find_element(By.XPATH, '/html/body/div[5]/div[1]/div/div/div/div/button[1]')
        save_calendar_button.click()
        time.sleep(1)
        input_text_reviews = driver.find_element(By.XPATH,
                                                 '/html/body/div[4]/div[1]/div/div/div/div/div/div/div[2]/div[5]/textarea')
        input_text_reviews.click()
        input_text_reviews.send_keys(list_review[0])
        list_review.remove(list_review[0])
        with open('for_negative_list_reviews.json', 'w', encoding='UTF-8') as outfile:
            json.dump(list_review, outfile)
        send_review = driver.find_element(By.XPATH,
                                          '/html/body/div[4]/div[1]/div/div/div/div/div/div/div[2]/div[8]/button[2]')
        send_review.click()
        time.sleep(10)
    except Exception as e:
        driver.quit()
        print('e:', e)
    finally:
        driver.quit()
        with open(r'negative_reviews_id.json') as f:
            list_answer = json.load(f)
            for dicts in list_answer:
                if dicts.get(key) is None:
                    continue
                else:
                    dicts.get(key)[3]='+'
        with open('negative_reviews_id.json', 'w') as outfile:
            json.dump(list_answer, outfile)
    return


def auth(url):
    driver.get(url)
    cookies = pickle.load(open(f'../cookies_mpboost.py', 'rb'))
    for cookie in cookies:
        driver.add_cookie(cookie)
    time.sleep(5)
    return '+'


def revizor(today,yesterday):
    dict_article = {}
    with open(r'negative_reviews_id.json') as f:
        list_answer = json.load(f)
    for dicts in list_answer:
        for key in dicts:
            if dicts.get(key)[2] == today or dicts.get(key)[2] == yesterday:
                if dicts.get(key)[3] == '-':
                    dict_article[key] = dicts.get(key)[0]
            else:
                continue
    return dict_article


if __name__ == "__main__":
    with open('for_negative_list_reviews.json') as f:
        list_review = json.load(f)
    if len(list_review) == 0:
        bot_alert_list_feed(len(list_review))
        exit()
    elif len(list_review) <= 10:
        bot_alert_reviews(len(list_review))
    today,yesterday = str(dt.datetime.date(dt.datetime.now())), str(dt.datetime.date(dt.datetime.now())-dt.timedelta(days=1))
    date = dt.datetime.now()
    month = date.strftime('%m')
    month_dict = {'01': 'января', '02': 'февраля', '03': 'марта', '04': 'апреля', '05': 'мая', '06': 'июня',
                  '07': 'июля', '08': 'августа', '09': 'сентября', '10': 'октября', '11': 'ноября', '12': 'декабря'}
    month_name = month_dict.get(f'{month}')
    url = 'https://app.mpboost.pro/reviews'
    dict_articles = revizor(today,yesterday)
    if len(dict_articles) > 0:
        driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36'})
        if auth(url) == '+':
            for key in dict_articles:
                order_review(dict_articles.get(key), key, list_review)
        driver.quit()

