<template>
    <v-app>
        <v-main class="pa-5 basecolor basefont">

            <h2 class="pb-5">
                認証エラー
            </h2>

            <v-divider id="hr-white"></v-divider>

            <div class="py-3">
                <div class="my-3">
                    アクセスして頂いたアドレスと、
                    入力して頂いた生年月日、
                    または認証コードが一致しません。
                </div>

                <div class="my-3">
                    正しい情報を入力してください。
                </div>
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
