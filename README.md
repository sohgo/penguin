症例候補の初期入力のプロトタイプ
================================

## 起動方法

1. dockerを[使う](https://github.com/tanupoo/proto-pen-docker)。
2. dockerを使わない。ドキュメントが足りてないのでおすすめしません。

### dockerを使わない。

- MongoDBをローカルに動かす。
- 下記4つのモジュールを動かす。
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

## コンフィグ

TBD

server_address

macの場合

IPv6/IPv4: ""
IPv6のみ: "::"
IPv4のみ: "0.0.0.0"

## Google Accountでのメールの設定

- mmmain.py からメールを送信するため、どこかにメールサーバが必要になる。
- 例えば、gmailが使える。
    + Googleのアカウントを作る。
    + Googleアカウント→セキュリティ→安全性に低いアプリのアクセス
        →アクセスを有効にする。
    + Gmail→設定→すべての設定を表示→メール転送とPOP/IMAP→変更を保存

## UIのビルド

ここからなぜか、ですます調😱

- uiの下で行います。
- npmはインストール済みとします。

```
sh build.sh
```

build.shは 各step1,step2に対して下記コマンドを実行しています。

```
cd ui/step1
npm install
patch -p 0 -i ../vue-cli.patch
alias vue=`pwd`/node_modules/@vue/cli/bin/vue.js
npm run build
```

patchコマンドが動いていますが、これは disableAssetsSubdirを有効にしています。
vue-cliのバージョンによってはパッチが当たらない可能性もあります。
rejectされた場合は、下記2つを手で当ててください。

```
diff -u node_modules/@vue/cli-service/lib/util/getAssetPath.js.orig node_modules/@vue/cli-service/lib/util/getAssetPath.js 
--- node_modules/@vue/cli-service/lib/options.js.orig	1985-10-26 17:15:00.000000000 +0900
+++ node_modules/@vue/cli-service/lib/options.js	2021-05-28 13:16:35.000000000 +0900
@@ -1,6 +1,7 @@
 const { createSchema, validate } = require('@vue/cli-shared-utils')
 
 const schema = createSchema(joi => joi.object({
+  disableAssetsSubdir: joi.boolean(),
   publicPath: joi.string().allow(''),
   outputDir: joi.string(),
   assetsDir: joi.string().allow(''),
diff -u node_modules/@vue/cli-service/lib/util/getAssetPath.js.orig node_modules/@vue/cli-service/lib/util/getAssetPath.js
--- node_modules/@vue/cli-service/lib/util/getAssetPath.js.orig	1985-10-26 17:15:00.000000000 +0900
+++ node_modules/@vue/cli-service/lib/util/getAssetPath.js	2021-05-28 13:18:51.000000000 +0900
@@ -1,6 +1,9 @@
 const path = require('path')
 
 module.exports = function getAssetPath (options, filePath) {
+  if (options.disableAssetsSubdir === true) {
+    filePath = filePath.replace(/^css\//, '').replace(/^js\//, '')
+  }
   return options.assetsDir
     ? path.posix.join(options.assetsDir, filePath)
     : filePath
```

