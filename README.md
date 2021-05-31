症例候補の初期入力のプロトタイプ
================================

./dbmain.py db.conf.json
PEN_CONFIG_FILE=db.conf.json uvicorn dbmain:app --port 8082 

./femain.py fe.conf.json
PEN_CONFIG_FILE=fe.conf.json uvicorn femain:app --port 8081 

## Build

npmはインストール済みとします。

sh build.sh

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

## TODO

- requirements.txtを作る。
