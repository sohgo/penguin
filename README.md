症例候補の初期入力のプロトタイプ: バックエンド
==============================================

実装メモなどは[IMPLEMENTATION.md](https://github.com/tanupoo/penguin/blob/main/IMPLEMENTATION.md)を御覧ください。

UIは[こちら](https://github.com/tanupoo/penguin-ui)。

## 起動方法

1. dockerを[使う](https://github.com/tanupoo/penguin-docker)。
2. dockerを使わない。ドキュメントが足りてないのでおすすめしません。

### dockerを使わない。

- MongoDBをローカルに動かす。
- 下記5つのモジュールを動かす。
    + enmain.py
    + femain.py
    + mmmain.py
    + dbmain.py
    + admmain.py

起動方法は2通り。

```
./xxmain.py xx.conf.json
```

```
PEN_CONFIG_FILE=xx.conf.json uvicorn xxmain:app --port 808x 
```

上記 xxは fe, mm, db, adm に置き換える。

## コンフィグ

dockerの[コンフィグ例](https://github.com/tanupoo/penguin-docker)を
参考にする。

### server_address

- macの場合
    + IPv6/IPv4: ""
    + IPv6のみ: "::"
    + IPv4のみ: "0.0.0.0"

## Google Accountでのメールの設定

- mmmain.py からメールを送信するため、どこかにメールサーバが必要になる。
- 例えば、gmailが使える。
    + Googleのアカウントを作る。
    + Googleアカウント→セキュリティ→安全性に低いアプリのアクセス
        →アクセスを有効にする。
    + Gmail→設定→すべての設定を表示→メール転送とPOP/IMAP→変更を保存

