# 見たい映画を Discord と Google Sheet で管理するためのコード

## 準備

1. Discord Developer Portal にアクセスし[このサイト](https://note.com/exteoi/n/n00342a623c93)を参考に Bot を作成する．
1. Google Cloud Platform にアクセスし，[このサイト](https://amg-solution.jp/blog/26703)を参考に Google Sheet API の設定をする．

```json
{
  "DISCORD_TOKEN": "your_token"
}
```

```json
{
  "SPREADSHEET_ID": "huga",
  "SHEET_NAME": "poyo"
}
```

サイトからの情報をもとに以上の json を作成する．

```json
{
  "type": "service_account",
  "project_id": "fuga",
  "private_key_id": "hoge"
}
```

ダウンロードした json ファイルを同一ディレクトリに配置する．

## 使い方

```shell
uv run discord2sheet.py
```

を実行した状態で bot を追加したチャンネルで以下を入力すると使える．

- /want で見たいに追加
- /going で見る予定に追加,見たいに同じデータがあれば削除
- /watched で見たに追加,見たい，見る予定に同じデータがあれば削除
- /random でランダムなデータを見たいから取得
- /list コマンドでシートのすべてのデータを取得
  - /list-want コマンドで Want のデータを取得
  - /list-going コマンドで Going のデータを取得
  - /list-watched コマンドで Watched のデータを取得

改行することで複数入力ができる．
ex.)

```
/want movie1
movie2
```
