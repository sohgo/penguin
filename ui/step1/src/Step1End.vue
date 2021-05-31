<template>
    <v-app>
        <v-main class="pa-5 basecolor basefont">

            <h2 class="pb-5">
                初期情報を登録いたしました。<br>
                ご協力ありがとうございます。
            </h2>

            <v-divider id="hr-white"></v-divider>

            <div class="py-3">
                <div class="my-3">
                    次に個人情報<br>
                    を入力して頂きます。
                </div>

                <div class="my-3">
                    ご登録頂いたメールアドレスに<br>
                    入力フォームを送らせて頂きましたので、<br>
                    後から入力することも可能でございます。<br>
                </div>

                <div class="my-3">
                    ご確認下さい。
                </div>

            </div>

            <v-btn class="pa-5"
                   color="white"
                   block
                   @click="toDetailInput">
                <span class="black--text font-large">次にすすむ</span>
            </v-btn>

        </v-main>
    </v-app>
</template>

<script>
export default {
    methods: {
        toDetailInput: function() {
            let xpath = this.$store.state.formData.xpath
            let url = `${process.env.VUE_APP_SERVER_URL}/2/x/${xpath}`
            location.href = url
        },
    },
}
</script>

<style>
</style>
