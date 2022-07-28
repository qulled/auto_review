from operator import itemgetter
import os
from logging.handlers import RotatingFileHandler
from googleapiclient import discovery
from google.oauth2 import service_account
from googleapiclient.discovery import build
import logging
import requests
import json
import datetime as dt

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(BASE_DIR, 'logs/')
log_file = os.path.join(BASE_DIR, 'logs/pars_article_table.log')
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
SPREADSHEET_OPPONENT = os.getenv('SPREADSHEET_OPPONENT')


def get_feedback(rootId, skip):
    raw_data = {"imtId": rootId, "skip": skip, "take": 10, "order": "dateDesc"}
    url = "https://public-feedbacks.wildberries.ru/api/v1/summary/full"
    response = requests.post(
        url=url, headers={"Content-Type": "application/json"}, json=raw_data)
    response_message = response.json()
    for items in response_message["feedbacks"]:
        try:
            if int(items["productValuation"]) == 5:
                dict_answer = {}
                dict_answer[items["id"]] = 'ID'
                dict_answer["aricle"]  = items["nmId"]
                dict_answer["text"] = items["text"]
                dict_answer["date"] = items["createdDate"][:10].replace(
                    "T", " ")
                if find_by_key(list_feedback,items["id"]) == '+':
                    continue
                else:
                    list_feedback.append(dict_answer)
        except Exception as e:
            continue
        finally:
            newlist = sorted(list_feedback, key=itemgetter('date'), reverse=False)
            with open('opponent_feedbacks.json', 'w') as outfile:
                json.dump(newlist, outfile)
    return newlist

def find_by_key(iterable, key):
    for index, dict_ in enumerate(iterable):
        if key in dict_:
            return '+'


def search_rootId(imtId):
    url = (
            "https://card.wb.ru/cards/detail?spp=0&regions=68,64,83,4,38,80,33,70,82,86,75,30,69,22,66,31,48,1,40,71&stores=117673,122258,122259,125238,125239,125240,6159,507,3158,117501,120602,120762,6158,121709,124731,159402,2737,130744,117986,1733,686,132043&pricemarginCoeff=1.0&reg=0&appType=1&emp=0&locale=ru&lang=ru&curr=rub&couponsGeo=12,3,18,15,21&dest=-1029256,-102269,-1278703,-1255563&nm="
            + str(imtId)
            + ";64245978;64245979%27"
    )
    response = requests.get(url=url)
    response_message = response.json()
    for item in response_message["data"]["products"]:
        if item["id"] == imtId:
            rootId = int(item["root"])
    return rootId


def convert_to_column_letter(column_number):
    column_letter = ''
    while column_number != 0:
        c = ((column_number - 1) % 26)
        column_letter = chr(c + 65) + column_letter
        column_number = (column_number - c) // 26
    return column_letter


def feedbback_table(table_id, list_feedback):
    range_name = 'Авто'
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=table_id,
                                range=range_name, majorDimension='ROWS').execute()
    values = result.get('values', [])
    i = 1
    body_data = []
    if not values:
        logging.info('No data found.')
    else:
        try:
            for article in list_feedback:
                text = article.get('text')
                body_data += [
                    {'range': f'{range_name}!{convert_to_column_letter(1)}{i}',
                     'values': [[f'{text}']]}]
                i+=1
        except:
            pass
        finally:
            body = {
                'valueInputOption': 'USER_ENTERED',
                'data': body_data}
    sheet.values().batchUpdate(spreadsheetId=table_id, body=body).execute()




if __name__ == "__main__":
    try:
        with open('opponent_feedbacks.json') as f:
            list_feedback = json.load(f)
    except Exception as e:
        list_feedback = []
    date = dt.datetime.now()
    month = date.strftime('%m')
    year = date.strftime('%Y')
    today,yesterday = str(dt.datetime.date(dt.datetime.now())), str(dt.datetime.date(dt.datetime.now())-dt.timedelta(days=1))
    table_id = SPREADSHEET_OPPONENT
    list_articles = ['77866026']
    for article in list_articles:
        skip = 0
        try:
            while len(list_feedback) != 800:
                get_feedback(search_rootId(int(article)),skip)
                skip += 10
        except:
            pass
        finally:
            feedbback_table(table_id, list_feedback)