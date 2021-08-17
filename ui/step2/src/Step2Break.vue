<template>
    <v-app>

        <v-app-bar color="#03AF7A" class="text-center"
                   elevation="0"
                   dense
                   app>
            <v-btn icon @click="movePage('/Step2Input3')">
                <v-icon class="white--text"
                    link
                >mdi-arrow-left</v-icon>
            </v-btn>
            <v-spacer></v-spacer>
            <v-app-bar-title class="white--text">
            </v-app-bar-title>
            <v-spacer></v-spacer>
            <v-btn icon @click="movePage('/Step2Input4')">
                <v-icon class="white--text"
                    link
                >mdi-arrow-right</v-icon>
            </v-btn>
        </v-app-bar>

        <v-main class="entry-body white--text">

            <div class="mx-3 my-5">

                <h1 class="entry mb-3">
                    ありがとうございました。<br>
                    これで初期設定は終了です。
                </h1>

                <div class="my-5">
                    <div class="my-3">
                        ここで登録して頂いた情報は
                        保健師から連絡が入る前であれば、
                        メールまたはSMSでお送りさせて頂いたURLから、
                        いつでも変更ができます。
                    </div>

                    <div class="my-3">
                        この後、過去14日間の行動履歴を入力して頂くことになります。
                        大変ではありますが、新型コロナウイルス感染症の
                        感染拡大防止のため、できるだけ詳しく教えてください。
                    </div>

                    <div class="my-3">
                        また、今後毎日の体温や体調についても共有して頂きます。
                        こちらもご協力をよろしくお願いいたします。
                    </div>

                </div>

                <v-btn
                    class="pa-5"
                    color="white"
                    @click="movePage('/Step2Input4')"
                    block
                >
                    <span class="black--text">
                        次へすすむ
                    </span>
                </v-btn>


            </div>
        </v-main>
    </v-app>
</template>

<script>
//import utils from '@/common/utils.js'

export default {
    methods: {
        movePage: function(pageName) {
            this.$router.push(pageName)
        },
    }
}
</script>

<style>
</style>
