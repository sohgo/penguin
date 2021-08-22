#!/bin/sh

build()
{
    (
        target=$1
        echo "==== Building $target ===="
        cd ui/$target
        npm install
        patch -N -p 0 -i ../vue-cli.patch
        alias vue=`pwd`/node_modules/@vue/cli/bin/vue.js
        cp -r ../common src/
        npm run build
    )
}

case "$1" in
    1) build step1 ;;
    2) build step2 ;;
    *) 
        build step1
        build step2
        ;;
esac
