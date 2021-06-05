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
                個人情報の設定
            </v-app-bar-title>
            <v-spacer></v-spacer>
        </v-app-bar>

        <v-main class="white">
            <div class="ma-3">
                <h3 class="my-3">
                    あなたの氏名と誕生月日<br>
                    を入力して下さい。
                </h3>

                <v-divider id="hr-balck"></v-divider>

                <v-form ref="baseform"
                        v-model="valid"
                        class="mx-3"
                        lazy-validation
                        >
                    <v-text-field label="氏名"
                                    class="mt-3"
                                v-model="formData.name"
                                :rules="inputRequired"
                                required
                                ></v-text-field>
                    <v-row>
                        <v-col class="mt-3">誕生月日</v-col>
                        <v-col>
                            <v-select label="月"
                                    v-model="formData.birthM"
                                    :items="birthMList"
                                    :rules="selectRequired"
                                    required
                                    ></v-select>
                        </v-col>
                        <v-col>
                            <v-select label="日"
                                    v-model="formData.birthD"
                                    :items="birthDList"
                                    :rules="selectRequired"
                                    required
                                    ></v-select>
                        </v-col>
                    </v-row>
                    <v-text-field label="メールアドレス"
                                    class="mt-3"
                                    v-model="formData.emailAddr"
                                    :rules="emailAddrRules"
                                    required
                                    ></v-text-field>
                </v-form>

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
    components: {
    },
    data() {
        return {
            valid: false,
            birthMList: utils.monthsList,
            birthDList: utils.daysList,
            // Rules
            inputRequired: [utils.inputRequired],
            selectRequired: [utils.selectRequired],
            emailAddrRules: [utils.emailAddrCheck],
            formData: {}
        }
    },
    methods: {
        submitData: async function() {
            if (this.$refs.baseform.validate()) {
                let url = `${process.env.VUE_APP_SERVER_URL}/1`
                let response = await utils.async_post(url, this.formData)
                if (response.code == 201 && response.data.xpath) {
                    this.$store.state.formData.xpath = response.data.xpath
                    this.$router.push('/Step1End')
                } else {
                    this.$store.commit('updateResponseData', response)
                    this.$router.push('/Error')
                }
            }
        },
    },
    mounted: function() {
        this.formData = this.$store.state.formData
    }
}
</script>

<style>
</style>
