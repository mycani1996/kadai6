import os
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials

JSON_PATH = './data/service_key.json'
SHEET_NAME = 'テスト'

# スプレッドシートとの接続
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_PATH, scope)
gc = gspread.authorize(credentials)
worksheet = gc.open(SHEET_NAME).sheet1

# os.environ["SPREADSHEET_ID"]
# スプレッドシートの読み書き
worksheet.update_acell('A1', 'Hello World!')
print(worksheet.acell('A1'))