#!/bin/sh

build()
{
    target=$1
    echo "Building $target"
    cd ui/$target
    npm install
    patch -p 0 -i ../vue-cli.patch
    alias vue=`pwd`/node_modules/@vue/cli/bin/vue.js
    cp -r ../common src/
    npm run build
}

for d in step1 step2
do
    build $d
done
