import discord
import json

# JSONファイルからトークンを読み込む
with open("botKey.json", "r") as file:
    config = json.load(file)
    DISCORD_TOKEN = config["DISCORD_TOKEN"]

# Intentsの設定
intents = discord.Intents.default()
intents.message_content = True  # メッセージ内容を取得するためのIntent

# Discordクライアントの作成
client = discord.Client(intents=intents)


# Botが起動した際に実行されるイベント
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


# メッセージが投稿された際に実行されるイベント
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # 「こんにちは」に返信する
    if message.content == "こんにちは":
        await message.channel.send("こんにちは！")


# Botの実行
client.run(DISCORD_TOKEN)
