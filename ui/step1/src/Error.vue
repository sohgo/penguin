<template>
    <v-app>
        <v-main class="pa-5 basecolor basefont">

            <h2 class="pb-5">
                エラーが起きました。<br>
                {{this.$store.state.responseData.code}}
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
