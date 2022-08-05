import pickle
import re
import time
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from googleapiclient import discovery
from google.oauth2 import service_account
from googleapiclient.discovery import build
import logging
import os
import json
import datetime as dt
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(BASE_DIR, 'logs/')
log_file = os.path.join(BASE_DIR, 'logs/pars_stocks_table.log')
console_handler = logging.StreamHandler()
file_handler = RotatingFileHandler(
    log_file,
    maxBytes=100000,
    backupCount=3,
    encoding='utf-8'
)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s, %(levelname)s, %(message)s',
    handlers=(
        file_handler,
        console_handler
    )
)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CREDENTIALS_FILE = 'credentials_service.json'
credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE)
service = discovery.build('sheets', 'v4', credentials=credentials)
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
load_dotenv('.env ')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
SPREADSHEET_OPPONENT = os.getenv('SPREADSHEET_OPPONENT')
GH_TOKEN = os.getenv('GH_TOKEN')

def convert_to_column_letter(column_number):
    column_letter = ''
    while column_number != 0:
        c = ((column_number - 1) % 26)
        column_letter = chr(c + 65) + column_letter
        column_number = (column_number - c) // 26
    return column_letter


def get_feedback():
    list_review = []
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range='Отзывы LOTELOVE', majorDimension='ROWS').execute()
    values = result.get('values', [])
    try:
        if not values:
            logging.info('No data found.')
        else:
            for row in values[2:]:
                if len(row[0])> 10:
                    list_review.append(row[0])
    except:
        pass
    with open('negative_feedback/for_negative_list_reviews.json', 'w', encoding='UTF-8') as outfile:
        json.dump(list_review, outfile)


def get_article(table_id):
    with open('up_feedbacks/check_article.json', encoding='UTF-8') as f:
        dict_article = json.load(f)
    article_list = []
    for key_word in dict_article:
        article_list.append(key_word)
    month = dt.datetime.now().strftime('%m')
    year = dt.datetime.now().strftime('%Y')
    service = build('sheets', 'v4', credentials=credentials)
    sheet_metadata = service.spreadsheets().get(spreadsheetId=table_id).execute()
    for items in sheet_metadata['sheets']:
        range_name = items['properties'].get('title')
        if range_name != 'Лист1' and range_name != 'Авто':
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=table_id,
                                        range=range_name, majorDimension='COLUMNS').execute()
            values = result.get('values', [])
            for article in values[1]:
                if article.isdigit():
                    service = build('sheets', 'v4', credentials=credentials)
                    sheet = service.spreadsheets()
                    result = sheet.values().get(spreadsheetId='1LMqyN5w81xnRfvNf0CE75ozH7zMcTLhvYiNjTxHDURo',
                                                range=f'{month}.{year}', majorDimension='ROWS').execute()
                    values = result.get('values', [])
                    for row in values[2:]:
                        try:
                            a_article = row[6]
                            if a_article == article and a_article not in article_list:
                                dict_article[article] = [row[3].replace('\n',' '),row[5],range_name,'+']
                        except Exception as e:
                            pass
    with open(f'up_feedbacks/check_article.json', 'w', encoding='UTF-8') as outfile:
        json.dump(dict_article, outfile,ensure_ascii=False)
    return dict_article


def final_dict(url):
    options = Options()

    prefs = {'download.default_directory': r'C:\Users\ikaty\PycharmProjects\parser_margin\excel_docs'}

    options.add_argument("--start-maximized")
    # options.add_argument('--headless')
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.get(url)
    cookies = pickle.load(open(f'cookies_mpboost.py', 'rb'))
    for cookie in cookies:
        driver.add_cookie(cookie)
    time.sleep(5)
    with open('up_feedbacks/check_article.json') as f:
        dict_article = json.load(f)
    for key_word in dict_article:
        article = key_word
        search_article_button = driver.find_element(By.TAG_NAME, 'input')
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
        if soup.findAll('p', text = re.compile('Доступных отзывов нет')):
            if dict_article.get(key_word)[3]!='1':
                dict_article.get(key_word)[3] = '-'
            else:
                dict_article.get(key_word)[3] != '+'
        search_article_button = driver.find_element(By.TAG_NAME, 'input')
        search_article_button.click()
        time.sleep(1)
        search_article_button.send_keys(Keys.CONTROL, 'a')
        time.sleep(1)
        search_article_button.send_keys(Keys.BACKSPACE)
        with open(f'up_feedbacks/check_article.json', 'w') as outfile:
            json.dump(dict_article, outfile,ensure_ascii=False)
    driver.quit()
    return dict_article


def get_feedback_opponent(table_id):
    with open('up_feedbacks/check_article.json', 'r', encoding='UTF-8') as f:
        dict_article = json.load(f)
    for article in dict_article:
        range_name =dict_article.get(article)[2]
        print(range_name)
        list_reviews_opponent = []
        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=table_id,
                                    range=range_name, majorDimension='ROWS').execute()
        values = result.get('values', [])
        try:
            if not values:
                logging.info('No data found.')
            else:
                print(article)
                for row in values:
                    if len(row[0])> 10:
                        list_reviews_opponent.append(row[0])
        except Exception as e:
            print(e)
        with open(f'up_feedbacks/list_reviews_opponent_{article}.json', 'w', encoding='UTF-8') as outfile:
            json.dump(list_reviews_opponent, outfile,ensure_ascii=False)
    return


if __name__ == "__main__":
    url = 'https://app.mpboost.pro/reviews'
    table_id = SPREADSHEET_OPPONENT
    # get_feedback()
    # get_article(table_id)
    get_feedback_opponent(table_id)
    # final_dict('https://app.mpboost.pro/reviews')

