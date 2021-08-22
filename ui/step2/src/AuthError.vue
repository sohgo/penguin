<template>
    <v-app>

        <v-app-bar color="#03AF7A" class="text-center"
                   elevation="0"
                   dense
                   app>
            <v-btn icon @click="movePage('/auth')">
                <v-icon class="white--text"
                    link
                >mdi-arrow-left</v-icon>
            </v-btn>
            <v-spacer></v-spacer>
            <v-app-bar-title class="white--text">
                エラー
            </v-app-bar-title>
            <v-spacer></v-spacer>
            <v-btn icon disabled></v-btn>
        </v-app-bar>

        <v-main>

            <div class="mx-3 my-5">
                <h1 class="my-3">
                    認証コードに誤りがあります。
                </h1>

                <p>
                    正しいコードを入力してください。
                </p>

                <p>
                    {{this.$store.state.responseData}}
                </p>
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
    beforeEach: function(to, from) {
        console.log(`to:${to.name} from:${from.name}`)
    }
}
</script>

<style>
</style>
