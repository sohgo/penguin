<template>
    <v-app>
        <v-main class="pa-5 basecolor basefont">

            <h2 class="pb-5">
                ブラウザを閉じて下さい。
            </h2>

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
