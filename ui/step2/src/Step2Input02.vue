<template>
    <v-app>
        <v-app-bar color="#03AF7A" class="basefont white--text text-center"
                   elevation="0"
                   dense
                   app>
            <v-spacer></v-spacer>
            <v-app-bar-title>
                個人情報の入力２
            </v-app-bar-title>
            <v-spacer></v-spacer>
        </v-app-bar>

        <v-main class="subcolor basefont">
            <div class="mx-3 my-5">
                <h3 class="my-3">
                    あなたのXXX<br>
                    についてお伺いします。
                </h3>

                <v-divider id="hr-balck"></v-divider>

                続きの質問がここに入る。

                <v-btn class="pa-5"
                       color="#03AF7A"
                       @click="nextPage"
                       block
                       >
                    <span class="pa-2 white--text font-large">
                        次へすすむ
                    </span>
                </v-btn>
            </div>
        </v-main>

    </v-app>
</template>

<script>
import utils from '@/common/utils.js'

export default {
    data() {
        return {
            formData: {},
        }
    },
    methods: {
        nextPage: function() {
            if (this.$refs.baseform.validate()) {
                this.$store.commit('updateFormData', this.formData)
                this.$router.push('/Step2End')
            }
        },
    },
    mounted: function() {
        this.formData = this.$store.state.formData
        console.log("formData", this.formData)
    }
}
</script>

<style>
</style>
