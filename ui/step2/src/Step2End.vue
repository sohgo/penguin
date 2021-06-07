<template>
    <v-app>
        <v-app-bar color="#03AF7A" class="basefont white--text text-center"
                   elevation="0"
                   dense
                   app>
        </v-app-bar>

        <v-main class="basecolor basefont">
            <div class="mx-5">

                <h3 class="mb-5">
                    ありがとうございました。<br>
                    これで初期設定は終了です。
                </h3>

                <v-divider id="hr-white"></v-divider>

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

                <v-btn class="pa-5"
                        color="white"
                        @click="closeWindow"
                        block
                        >
                    <span class="pa-2 black--text font-large">ウィンドウを閉じる</span>
                </v-btn>

            </div>
        </v-main>
    </v-app>
</template>

<script>
//import utils from '@/common/utils.js'

export default {
    methods: {
        closeWindow: function() {}
    }
}
</script>

<style>
</style>
