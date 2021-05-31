<template>
    <v-app>
        <div class="font">
            <v-app-bar class="basecolor text-center white--text" dense>
                <v-btn icon to="/">
                    <v-icon class="white--text"
                        link
                        >mdi-arrow-left</v-icon>
                </v-btn>
                <v-spacer></v-spacer>
                <v-app-bar-title class="white--text">
                    認証情報の入力
                </v-app-bar-title>
                <v-spacer></v-spacer>
            </v-app-bar>

            <v-main class="grey lighten-5">
                <div class="ma-3">
                    登録時に入力した誕生月日と好みの色を選択して下さい。
                </div>
                <v-form ref="baseform"
                        v-model="valid"
                        class="mx-3"
                        lazy-validation
                        >
                    <v-row>
                        <v-col class="mt-3">誕生月日</v-col>
                        <v-col>
                            <v-select label="月"
                                    v-model="formData.birthM"
                                    :items="birthMList"
                                    :rules="selectRequired"
                                    required
                                    >
                            </v-select>
                        </v-col>
                        <v-col>
                            <v-select label="日"
                                    v-model="formData.birthD"
                                    :items="birthDList"
                                    :rules="selectRequired"
                                    required
                                    >
                            </v-select>
                        </v-col>
                    </v-row>
                    <v-select label="好みの色"
                              class="mb-3"
                              v-model="formData.favColor"
                              :items="favColorList"
                              :rules="selectRequired"
                              required
                              >
                    </v-select>
                </v-form>
                <v-btn class="teal accent-4 white--text"
                       @click="sendAuth"
                       block
                       >
                    <span class="ft-large">送信する</span>
                </v-btn>
            </v-main>
        </div>
    </v-app>
</template>

<script>
import utils from '@/utils.js'

export default {
    components: {
    },
    data() {
        return {
            valid: false,
            selectRequired: [utils.selectRequired],
            birthMList: utils.monthsList,
            birthDList: utils.daysList,
            favColorList: utils.colorsList,
            formData: {},
        }
    },
    methods: {
        sendAuth: async function() {
            if (this.$refs.baseform.validate()) {
                let url = `${process.env.VUE_APP_SERVER_URL}/a`
                let response = await utils.async_post(url, this.formData)
                if (response.code == 200) {
                    this.$store.state.formData = response.data
                    this.$router.push('/Step2Input')
                } else if (response.code == 406) {
                    this.$router.push('/AuthError')
                } else {
                    this.$store.commit('updateResponseData', response)
                    this.$router.push('/Error')
                }
            }
        },
    },
    mounted: function() {
        this.formData = this.$store.state.formData
        let url = document.URL
        this.formData.xpath = url.slice(url.indexOf('/2/x/')+5, url.indexOf('#/Auth'))
        console.log("formData", this.formData)
    }
}
</script>

<style>
</style>
