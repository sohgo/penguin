<template>
    <v-app>

        <v-app-bar color="#03AF7A" class="text-center"
                   elevation="0"
                   dense
                   app>
            <v-btn icon @click="movePage('/daily')">
                <v-icon class="white--text"
                    link
                >mdi-arrow-left</v-icon>
            </v-btn>
            <v-spacer></v-spacer>
            <v-app-bar-title class="white--text">
            </v-app-bar-title>
            <v-spacer></v-spacer>
            <v-btn icon disabled></v-btn>
        </v-app-bar>

        <v-main class="entry-body white--text">

            <div class="mx-3 my-5">

                <h1 class="entry mb-3">
                    ご協力、ありがとうございました。
                </h1>

                <div class="my-5">
                    <div class="my-3">
                        ここで登録して頂いた情報は
                        保健師から連絡が入る前であれば、
                        メールでお送りさせて頂いたURLから、
                        いつでも変更することができます。
                    </div>

                </div>

            </div>
        </v-main>

    </v-app>
</template>

<script>
export default {
    methods: {
        movePage: function(pageName) {
            this.$router.push(pageName)
        }
    },
    beforeEach(to, from) {
        console.log(`to:${to.name} from:${from.name}`)
    }
}
</script>

<style>
</style>
