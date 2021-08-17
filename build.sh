#!/bin/sh

build()
{
    target=$1
    cd ui/$target
    npm install
    patch -N -p 0 -i ../vue-cli.patch
    alias vue=`pwd`/node_modules/@vue/cli/bin/vue.js
    cp -r ../common src/
    npm run build
}

for d in step1 step2
do
    target=$d
    echo "==== Building $target ===="
    (build $target)
done
