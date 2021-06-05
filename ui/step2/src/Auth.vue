<template>
    <v-app>
        <v-app-bar color="#03AF7A" class="basefont white--text text-center"
                   elevation="0"
                   dense
                   app>
            <v-btn icon to="/">
                <v-icon class="white--text"
                    link
                    >mdi-arrow-left</v-icon>
            </v-btn>
            <v-spacer></v-spacer>
            <v-app-bar-title>
                認証情報の入力
            </v-app-bar-title>
            <v-spacer></v-spacer>
        </v-app-bar>

        <v-main class="grey lighten-5">
            <div class="ma-3">
                <h3 class="my-3">
                    登録時に入力した誕生月日と、<br>
                    メールでお送りした認証コード<br>
                    （3組の4桁の数字）を<br>
                    入力して下さい。
                </h3>

                <v-form ref="baseform"
                        v-model="valid"
                        class="mx-3"
                        lazy-validation
                        >
                    <v-row>
                        <v-col class="mt-3">誕生月日</v-col>
                        <v-col class="mt-0">
                            <v-select label="月"
                                    v-model="formData.birthM"
                                    :items="birthMList"
                                    :rules="selectRequired"
                                    required
                                    >
                            </v-select>
                        </v-col>
                        <v-col class="mt-0">
                            <v-select label="日"
                                    v-model="formData.birthD"
                                    :items="birthDList"
                                    :rules="selectRequired"
                                    required
                                    >
                            </v-select>
                        </v-col>
                    </v-row>

                    <!-- 認証コード -->
                    <v-row class="mt-3">
                        <v-col class="mt-3 mx-0">認証コード</v-col>
                    </v-row>
                    <v-row class="mx-1 mt-0"> 

                        <v-col class="pa-0 ma-0 accol">
                            <v-text-field
                                class="text-h6 acfield"
                                ref="ac1"
                                v-model="ac1"
                                :rules="acRequired"
                                placeholder="0000"
                                required
                                >
                            </v-text-field>
                        </v-col>
                        <span class="pa-0 mx-1 mt-3 acdash">―</span>
                        <v-col class="pa-0 ma-0 accol">
                            <v-text-field
                                class="text-h6 acfield"
                                ref="ac2"
                                v-model="ac2"
                                :rules="acRequired"
                                placeholder="0000"
                                required
                                >
                            </v-text-field>
                        </v-col>
                        <span class="pa-0 mx-1 mt-3 acdash">―</span>
                        <v-col class="pa-0 ma-0 accol">
                            <v-text-field
                                class="text-h6 acfield"
                                ref="ac3"
                                v-model="ac3"
                                :rules="acRequired"
                                placeholder="0000"
                                required
                                >
                            </v-text-field>
                        </v-col>
                    </v-row>

                </v-form>

                <v-btn class="pa-5"
                       color="#03AF7A"
                       @click="sendAuth"
                       block
                       >
                    <span class="pa-2 white--text font-large">
                        送信する
                    </span>
                </v-btn>
            </div>
        </v-main>

    </v-app>
</template>

<script>
import utils from '@/common/utils.js'

export default {
    components: {
    },
    data() {
        return {
            valid: false,
            selectRequired: [utils.selectRequired],
            birthMList: utils.monthsList,
            birthDList: utils.daysList,
            acRequired: [
                v => !!v || '認証コードは必須です。',
                v => /\d{4}/.test(v) || '4桁の数字を入力して下さい。'
            ],
            formData: {},
            ac1: '',
            ac2: '',
            ac3: ''
        }
    },
    methods: {
        sendAuth: async function() {
            if (this.$refs.baseform.validate()) {
                // make authcode properly.
                this.formData.authcode = `${this.ac1}-${this.ac2}-${this.ac3}`
                // submit formData.
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
    watch: {
        ac1(v) { if (v.length >= 4) { this.$refs.ac2.focus() } },
        ac2(v) { if (v.length >= 4) { this.$refs.ac3.focus() } },
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
.accol {
    width: 20%;
    max-width: 20%;
    flex-basis: 20%;
}
.acfield input {
    text-align: center;
}
.acfield input::placeholder {
    text-align: center;
}
.acdash {
    width: 4%;
    max-width: 4%;
    flex-basis: 4%;
}

</style>
