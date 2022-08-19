from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from googleapiclient import discovery
from google.oauth2 import service_account
from googleapiclient.discovery import build
import logging
import os
import random
import json


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(BASE_DIR, 'logs/')
log_file = os.path.join(BASE_DIR, 'logs/gen_rev.log')
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
SPREADSHEET_ID_GENERATOR = os.getenv('SPREADSHEET_ID_GENERATOR')


def convert_to_column_letter(column_number):
    column_letter = ''
    while column_number != 0:
        c = ((column_number - 1) % 26)
        column_letter = chr(c + 65) + column_letter
        column_number = (column_number - c) // 26
    return column_letter


def get_article(table_id):
    article_dict = {}
    article = ''
    service = build('sheets', 'v4', credentials=credentials)
    sheet_metadata = service.spreadsheets().get(spreadsheetId=table_id).execute()
    for items in sheet_metadata['sheets']:
        range_name = items['properties'].get('title')
        if range_name != 'generation':
            for i in range_name:
                if i.isdigit():
                    article+=i
                else:
                    break
            article_dict[article] = range_name
            article = ''
    print(article_dict)
    return article_dict


def get_phrase(table_id,article,article_name):
    try:
        with open(f'up_feedbacks/list_reviews_opponent_{article}.json', 'r', encoding='UTF-8') as f:
            list_reviews = json.load(f)
    except:
        list_reviews = []
    accept = 0
    while accept == 0:
        text = ''
        emoji = ['❤','💓','🖤','💕','🔥','😍','😍','❤','🥰','🔥','🥰','💕','💓','😍','🥰','😻','❤','😻','💓','😻','😍','🥰','😻']
        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=table_id,
                                    range=article_name, majorDimension='COLUMNS').execute()
        values = result.get('values', [])
        emoji_random = random.randint(0,len(emoji)-1)
        get_start_column = random.randint(0,10)
        if get_start_column > 7:
            get_start_word = random.randint(1,11)
            text+=(values[1][get_start_word])
            get_start_word_2 = random.randint(1,12)
            text+=(values[3][get_start_word_2])
            rand_get = random.randint(0, 5)
            if rand_get > 3:
                text += f' {emoji[emoji_random]}'
            rand_get = random.randint(1, 3)
            if rand_get < 3:
                get_text_up = random.randint(1,9)
                text += (values[6][get_text_up])
                get_text_up_up = random.randint(1,9)
                text += (values[7][get_text_up_up])
            rand_get = random.randint(1,3)
            if rand_get < 3:
                get_mestoimenie = random.randint(1,10)
                text += (values[10][get_mestoimenie])
                get_final = random.randint(1,10)
                text += (values[11][get_final])
        else:
            text+=values[0][random.randint(1,10)]
            get_start_word_2 = random.randint(1, 13)
            if text == ' ':
                text=text.strip()
                text += values[2][get_start_word_2].capitalize()
            else:
                text+=values[2][get_start_word_2]
            get_up_word = random.randint(1,12)
            text+=values[4][get_up_word]
            get_up_up_word = random.randint(1, 5)
            text += values[5][get_up_up_word]
            rand_get = random.randint(0, 5)
            if rand_get > 3:
                text += f' {emoji[emoji_random]}'
            rand_get = random.randint(1,3)
            if rand_get < 3:
                up_word = random.randint(1, 14)
                text += values[8][up_word]
                up_up_word = random.randint(1, 10)
                text += values[9][up_up_word]
        rand_get = random.randint(1,10)
        if rand_get < 4:
            text+= f'{emoji[emoji_random]*random.randint(1,3)}'
        if text not in list_reviews:
            list_reviews.append(text)
            with open(f'up_feedbacks/list_reviews_opponent_{article}.json', 'w', encoding='UTF-8') as outfile:
                json.dump(list_reviews, outfile,ensure_ascii=False)
            accept = 1
    return print(text)


if __name__ == "__main__":
    table_id = SPREADSHEET_ID_GENERATOR
    article_dict = get_article(table_id)
    for article in article_dict:
        get_phrase(table_id,article,article_name=article_dict.get(article))
