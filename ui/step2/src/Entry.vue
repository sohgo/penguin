<template>
    <v-app>

        <v-main class="entry-body white--text">

            <div class="mx-3 my-5">

                <h1 class="entry my-3">
                    積極的疫学調査<br>
                    にご協力ください。
                </h1>

                <div class="py-3">
                    <div class="my-3">
                        このたびは新型コロナウイルス感染症に罹患され、
                        大変ご不安だと思います。
                    </div>

                    <div class="my-3">
                        このアプリではあなたがこれまでにどのような方と
                        接触してきたのか、また、毎日の体調について
                        共有して頂くためのインタフェースを提供しています。
                    </div>

                    <div class="my-3">
                        アプリを使い始める前に、
                        <div class="ma-2">
                        1. あなたの住所などの情報<br>
                        2. 基礎疾患に関する情報<br>
                        </div>
                        について登録をお願いします。
                    </div>

                    <div class="my-3">
                        その後、過去14日間の行動履歴について、
                        このアプリに登録をして頂きます。
                    </div>

                    <div class="my-3">
                        少し時間のかかる作業ではありますが、
                        新型コロナウイルス感染症の拡大を防止
                        するために必要ですので、休憩を取りながら、
                        できるだけ正確な情報の登録を
                        お願いします。
                    </div>

                    <div class="my-3">
                        よろしくお願いいたします。
                    </div>
                </div>

                <v-btn
                    class="pa-5"
                    color="white"
                    to="/Auth"
                    block
                >
                    <span class="black--text">
                        はじめる
                    </span>
                </v-btn>

            </div>
        </v-main>

    </v-app>
</template>

<script>
export default {
}
</script>

<style>
.entry-body {
    background-color: #03AF7A;
}
</style>
