import gspread
from google.oauth2.service_account import Credentials
import json

# JSONファイルからトークンを読み込む
with open("botKey.json", "r") as file:
    config = json.load(file)
    DISCORD_TOKEN = config["DISCORD_TOKEN"]


# Google Sheets APIの認証設定
scope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("googleKey.json", scopes=scope)
client = gspread.authorize(creds)

# GoogleスプレッドシートのIDとシート名
# JSONファイルからトークンを読み込む
with open("googleSheetData.json", "r") as file:
    config = json.load(file)
    SPREADSHEET_ID = config["SPREADSHEET_ID"]
    SHEET_NAME = config["SHEET_NAME"]
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

# データをスプレッドシートに書き込む例
data = ["Sample User", "Hello, World!", "2024-11-07"]
sheet.append_row(data)

# スプレッドシートからデータを読み込む例
rows = sheet.get_all_records()
print(rows)
