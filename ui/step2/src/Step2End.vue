<template>
    <v-app>
        <v-app-bar color="#03AF7A" class="basefont white--text text-center"
                   elevation="0"
                   dense
                   app>
            <v-btn icon to="/BaseInput">
                <v-icon class="white--text"
                    link
                    >mdi-arrow-left</v-icon>
            </v-btn>
            <!--
            <v-spacer></v-spacer>
            <v-app-bar-title>
                個人情報の設定
            </v-app-bar-title>
            <v-spacer></v-spacer>
            -->
        </v-app-bar>

        <v-main class="basecolor basefont">
            <div class="mx-5">

                <h2 class="mb-5">
                    ありがとうございました。<br>
                    これで初期設定は終了です。
                </h2>

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
                        @click="submitData"
                        block
                        >
                    <span class="pa-2 black--text font-large">完了</span>
                </v-btn>

            </div>
        </v-main>
    </v-app>
</template>

<script>
import utils from '@/common/utils.js'

export default {
    methods: {
        submitData: async function() {
            // XXX この部分は他の入力の最後に持っていくべき。
            //
            let url = `${process.env.VUE_APP_SERVER_URL}/2`
            let response = await utils.async_post(url, this.$store.state.formData)
            console.log(`RES: ${response.code}`)
            if (response.code == 200) {
                // 成功したら、それ以降の操作を無効にするためにxpathを消す。
                this.formData.xpath = ''
                this.$router.push('/End')
            } else {
                this.$store.commit('updateResponseData', response)
                this.$router.push('/Error')
            }
        }
    }
}
</script>

<style>
</style>
