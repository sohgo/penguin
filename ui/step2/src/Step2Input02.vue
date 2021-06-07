<template>
    <v-app>
        <v-app-bar color="#03AF7A" class="basefont white--text text-center"
                   elevation="0"
                   dense
                   app>
            <v-btn icon to="/Step2Input">
                <v-icon class="white--text"
                    link
                    >mdi-arrow-left</v-icon>
            </v-btn>
            <v-spacer></v-spacer>
            <v-app-bar-title>
                個人情報の入力２
            </v-app-bar-title>
            <v-spacer></v-spacer>
        </v-app-bar>

        <v-main class="subcolor basefont">
            <div class="mx-3 my-5">
                <h3 class="my-3">
                    あなたの基礎疾患<br>
                    についてお伺いします。
                </h3>

                <v-divider id="hr-balck"></v-divider>

                <v-form ref="baseform"
                        v-model="valid"
                        class="mx-3"
                        lazy-validation
                        >
                    該当する疾患についてチェックしてください。
                    <v-checkbox label="妊娠中"
                                v-model="formData.pregnant"
                                >
                    </v-checkbox>
                    <v-row align="left">
                            <v-checkbox label="喫煙"
                                        v-model="formData.smoker"
                                        class="shrink mr-2 mt-0"
                                        ></v-checkbox>
                            <v-text-field
                                label="何歳から１日あたり何本吸いますか？"
                                :disabled="!smoker"
                                v-model="formData.smokerDetail"
                            ></v-text-field>
                    </v-row>

                </v-form>

                <h3>
                    続きの質問がここに入る。
                </h3>

                <v-btn class="pa-5"
                       color="#03AF7A"
                       @click="submitData"
                       block
                       >
                    <span class="pa-2 white--text font-large">
                        登録する
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
        submitData: async function() {
            if (this.$refs.baseform.validate()) {
                this.$store.commit('updateFormData', this.formData)
                let url = `${process.env.VUE_APP_SERVER_URL}/2`
                let response = await utils.async_post(url, this.$store.state.formData)
                if (response.code == 200) {
                    // 成功したら以降の操作を無効にするためにformDataを消す。
                    this.$store.state.formData = {}
                    this.$router.push('/Step2End')
                } else {
                    // エラーの場合、responseを保存する。要考察。
                    this.$store.commit('updateResponseData', response)
                    this.$router.push('/Error')
                }
            }
        }
    },
    mounted: function() {
        this.formData = this.$store.state.formData
        console.log("formData", this.formData)
    }
}
</script>

<style>
</style>
