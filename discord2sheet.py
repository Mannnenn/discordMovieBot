import discord
import json
import random
import gspread
from google.oauth2.service_account import Credentials

# 1     2       3
# Want	Going	Watched

help_message = """
- /want で見たいに追加
- /going で見る予定に追加,見たいに同じデータがあれば削除
- /watched で見たに追加,見たい，見る予定に同じデータがあれば削除
- /random でランダムなデータを見たいから取得
- /listコマンドでシートのすべてのデータを取得
  - /list-wantコマンドでWantのデータを取得
  - /list-goingコマンドでGoingのデータを取得
  - /list-watchedコマンドでWatchedのデータを取得
"""


# Intentsの設定
intents = discord.Intents.default()
intents.message_content = True  # メッセージ内容を取得するためのIntent

# Discordクライアントの作成
client = discord.Client(intents=intents)


# JSONファイルからトークンを読み込む
with open("botKey.json", "r") as file:
    config = json.load(file)
    DISCORD_TOKEN = config["DISCORD_TOKEN"]

# Google Sheets APIの認証設定
scope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("googleKey.json", scopes=scope)
gs_client = gspread.authorize(creds)

# GoogleスプレッドシートのIDとシート名
with open("googleSheetData.json", "r") as file:
    config = json.load(file)
    SPREADSHEET_ID = config["SPREADSHEET_ID"]
    SHEET_NAME = config["SHEET_NAME"]
sheet = gs_client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # 10回に1回のみ実行する
    if random.randint(1, 10) == 1:
        # 実行されるたびに余計な空白を詰めていく
        rows = sheet.get_all_values()
        # 列ごとに空白を詰める
        columns = list(zip(*rows))
        cleaned_columns = []
        for column in columns:
            cleaned_column = [cell for cell in column if cell.strip()]
            cleaned_column.extend([""] * (len(column) - len(cleaned_column)))
            cleaned_columns.append(cleaned_column)
        cleaned_rows = list(zip(*cleaned_columns))
        sheet.clear()
        for row in cleaned_rows:
            sheet.append_row(row)

    # "/want"コマンドで指定されたデータをA列に追記
    if message.content.startswith("/want"):
        data = message.content[len("/want ") :]
        await message.channel.send(f"Added to Want: {data}")
        rows = data.split("\n")
        for row in rows:
            sheet.append_row([row, "", ""])  # A列にデータを追加、他の列は空白

    # "/going"コマンドで指定されたデータをB列に追記,A列に同じデータがあれば削除
    elif message.content.startswith("/going"):
        data = message.content[len("/going ") :]
        await message.channel.send(f"Added to Going: {data}")
        rows = data.split("\n")
        for row in rows:
            # A列に同じデータがあれば削除
            cell = sheet.find(row, in_column=1)
            if cell:
                sheet.delete_rows(cell.row)
            # B列にデータを追加、他の列は空白
            sheet.append_row(["", row, ""])

    # "/watched"コマンドで指定されたデータをC列に追記,1,2列目に同じデータがあれば削除
    elif message.content.startswith("/watched"):
        data = message.content[len("/watched ") :]
        await message.channel.send(f"Added to Watched: {data}")
        rows = data.split("\n")
        for row in rows:
            # 1,2列目に同じデータがあれば削除
            cell_a = sheet.find(row, in_column=1)
            cell_b = sheet.find(row, in_column=2)
            if cell_a:
                sheet.delete_rows(cell_a.row)
            if cell_b:
                sheet.delete_rows(cell_b.row)
            # C列にデータを追加、他の列は空白
            sheet.append_row(["", "", row])

    # "/random"コマンドでランダムなデータを1列目から取得
    elif message.content.startswith("/random"):
        # シートの1列目のデータを取得
        column_data = sheet.col_values(1)
        # ヘッダーを除いたデータ部分のみを取得
        data = column_data[1:]
        # ランダムに1つ選択
        random_data = random.choice(data)
        # メッセージを送信
        await message.channel.send(random_data)

    # "/list"コマンドでシートのすべてのデータを取得
    # "/list-want"コマンドでWantのデータを取得
    # "/list-going"コマンドでGoingのデータを取得
    # "/list-watched"コマンドでWatchedのデータを取得
    elif message.content.startswith("/list"):
        # シートのデータを取得
        rows = sheet.get_all_records()
        # Embedメッセージを作成
        embed = discord.Embed(title="Sheet Data", color=0x3498DB)

        # Wantの値を抽出して結合
        want_values = "\n".join([str(row["Want"]) for row in rows if row["Want"]])

        # Goingの値を抽出して結合
        going_values = "\n".join([str(row["Going"]) for row in rows if row["Going"]])

        # Watchedの値を抽出して結合
        watched_values = "\n".join(
            [str(row["Watched"]) for row in rows if row["Watched"]]
        )

        if message.content.startswith("/list-want"):
            embed.add_field(name="Want", value=want_values or "No data", inline=True)
        elif message.content.startswith("/list-going"):
            embed.add_field(name="Going", value=going_values or "No data", inline=True)
        elif message.content.startswith("/list-watched"):
            embed.add_field(
                name="Watched", value=watched_values or "No data", inline=True
            )
        else:
            embed.add_field(name="Want", value=want_values or "No data", inline=True)
            embed.add_field(name="Going", value=going_values or "No data", inline=True)
            embed.add_field(
                name="Watched", value=watched_values or "No data", inline=True
            )

        # メッセージを送信
        await message.channel.send(embed=embed)

    elif message.content.startswith("/help"):
        # ヘルプメッセージを送信
        await message.channel.send(help_message)


# Botの実行
client.run(DISCORD_TOKEN)
