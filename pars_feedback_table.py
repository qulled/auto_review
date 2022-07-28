from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from googleapiclient import discovery
from google.oauth2 import service_account
from googleapiclient.discovery import build
import logging
import os
import json



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
    articles = {}
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
                    articles[range_name]=article
    return articles


def get_feedback_opponent(table_id,dict_article):
    for keyword in dict_article:
        article = dict_article.get(keyword)
        list_reviews_opponent = []
        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=table_id,
                                    range=keyword, majorDimension='ROWS').execute()
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
            json.dump(list_reviews_opponent, outfile)
    return


if __name__ == "__main__":
    table_id = SPREADSHEET_OPPONENT
    # get_feedback()
    get_feedback_opponent(table_id, get_article(table_id))

