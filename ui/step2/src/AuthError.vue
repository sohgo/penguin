<template>
    <v-app>

        <v-app-bar color="#03AF7A" class="text-center"
                   elevation="0"
                   dense
                   app>
            <v-btn icon @click="movePage(-1)">
                <v-icon class="white--text"
                    link
                >mdi-arrow-left</v-icon>
            </v-btn>
            <v-spacer></v-spacer>
            <v-app-bar-title class="white--text">
                認証エラー
            </v-app-bar-title>
            <v-spacer></v-spacer>
            <v-btn icon disabled></v-btn>
        </v-app-bar>

        <v-main>
            <div class="mx-3 my-5">
                <h1 class="my-3">
                    認証エラー
                </h1>

                <p>
                    アクセスして頂いたアドレスと、
                    認証コードが一致しません。
                </p>

                <p>
                    正しい情報を入力してください。
                </p>
            </div>
        </v-main>

    </v-app>
</template>

<script>
export default {
    beforeEach: function(to, from) {
        console.log(`to:${to.name} from:${from.name}`)
    }
}
</script>

<style>
</style>
