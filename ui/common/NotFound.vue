<template>
    <v-app>
        <v-app-bar color="#03AF7A" class="text-center"
                   elevation="0"
                   dense
                   app>
            <v-btn icon disabled></v-btn>
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
                    URLに誤りがあります。
                </h1>
            </div>

        </v-main>
    </v-app>
</template>

<script>
export default {
    beforeEach(to, from) {
        console.log(`to:${to.name} from:${from.name}`)
    }
}
</script>

<style>
</style>
