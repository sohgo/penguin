<template>
    <v-app>

        <v-main class="entry-body white--text">

            <div class="mx-3 my-5">

                <h1 class="entry my-3">
                    ご協力ありがとうございます。
                </h1>

                <div class="py-3">
                    <div class="my-3">
                        次に感染症対策に必要な情報<br>
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

                <v-btn
                    class="pa-5"
                    color="white"
                    block
                    @click="toDetailInput"
                >
                    <span class="black--text">
                        次にすすむ
                    </span>
                </v-btn>

            </div>
        </v-main>
    </v-app>
</template>

<script>
export default {
    methods: {
        toDetailInput: function() {
            location.href = this.$store.state.url
        },
    },
}
</script>

<style>
</style>
