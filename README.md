症例候補の初期入力のプロトタイプ: バックエンド
==============================================

実装メモなどは[IMPLEMENTATION.md](https://github.com/tanupoo/penguin/blob/main/IMPLEMENTATION.md)を御覧ください。

UIは[こちら](https://github.com/tanupoo/penguin-ui)。

## NOTE

**重要**
今後は https://github.com/ffhs-dev で開発を進めることになりました。
FFHSはプライベートリポジトリなのでコードを見ることはできません。
ですので、このリポジトリは参照用として残しておきます。

## 起動方法

1. dockerを[使う](https://github.com/tanupoo/penguin-docker)。
2. dockerを使わない。

### dockerを使わない。

- MongoDBをローカルに動かす。

mongoDBだけdockerを使う場合の起動の例

```
mkdir mongodb
docker run --rm --name pen-mongo --publish 27017:27017 --volume mongodb:/data/db mongo:latest
```

- 下記5つのモジュールを動かす。
    + enmain.py: エントリ入力(step1)用バックエンドモジュール
    + femain.py: 患者情報入力(step2)用バックエンドモジュール
    + mmmain.py: メール送信モジュール
    + dbmain.py: dbインターフェイスモジュール
    + admmain.py: 管理インターフェイスモジュール

*module.py config_file*で起動する。

下記 xxは fe, mm, db, adm に置き換える。

```
./xxmain.py xx.conf.json
```

ASGI経由でも動かせる。

```
PEN_CONFIG_FILE=xx.conf.json uvicorn xxmain:app --port 808x 
```

enmain.pyの起動の例。

```
$ ./enmain.py en.conf.json
2023-05-12T05:14:50.548 26 DEBUG DEBUG mode
2023-05-12T05:14:50.548 9 INFO Starting PEN Step1 server listening on http://*:8000/
INFO:     Started server process [48888]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://:8000 (Press CTRL+C to quit)
```

## コンフィグ

dockerの[コンフィグ例](https://github.com/tanupoo/penguin-docker)を
参考にする。

## メールサーバについて

**gmailの運用方針が変わったため、現在は動作しない模様。(Oct-2022)**

- mmmain.py からメールを送信するため、どこかにメールサーバが必要になる。
- 例えば、gmailが使える。
    + Googleのアカウントを作る。
    + Googleアカウント→セキュリティ→安全性に低いアプリのアクセス
        →アクセスを有効にする。
    + Gmail→設定→すべての設定を表示→メール転送とPOP/IMAP→変更を保存

### server_address

- macの場合
    + IPv6/IPv4: ""
    + IPv6のみ: "::"
    + IPv4のみ: "0.0.0.0"

