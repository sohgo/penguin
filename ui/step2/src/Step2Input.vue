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
                個人情報の入力１
            </v-app-bar-title>
            <v-spacer></v-spacer>
        </v-app-bar>

        <v-main class="subcolor basefont">
            <div class="mx-3 my-5">
                <h3 class="my-3">
                    あなたの住所や勤務先・<br>
                    学校についてお伺いします。
                </h3>

                <v-divider id="hr-balck"></v-divider>

                <v-form ref="baseform"
                        v-model="valid"
                        class="mx-3 my-5"
                        lazy-validation
                        >
                    <v-row class="pb-0 mb-0">
                        <v-col>発症日</v-col>
                    </v-row>
                    <v-row class="pt-0 mt-0">
                        <v-col>
                            <v-select label="年"
                                    v-model="formData.onsetY"
                                    :items="onsetYList"
                                    >
                            </v-select>
                        </v-col>
                        <v-col>
                            <v-select label="月"
                                    v-model="formData.onsetM"
                                    :items="onsetMList"
                                    >
                            </v-select>
                        </v-col>
                        <v-col>
                            <v-select label="日"
                                    v-model="formData.onsetD"
                                    :items="onsetDList"
                                    >
                            </v-select>
                        </v-col>
                    </v-row>
                    <v-text-field label="氏名"
                                    class="mt-3"
                                    v-model="formData.name"
                                    :rules="inputRequired"
                                    disabled
                                    >
                    </v-text-field>
                    <v-row class="">
                        <v-col>生年月日</v-col>
                        <template v-slot:append-outer>
                            <v-badge content="必須" color="red" overlap>
                        </template>
                    </v-row>
                    <v-row class="pt-0 mt-0">
                        <v-col>
                            <v-select label="年"
                                    v-model.lazy="formData.birthY"
                                    :items="birthYList"
                                    :rules="selectRequired"
                                    >
                            </v-select>
                        </v-col>
                        <v-col>
                            <v-select label="月"
                                    v-model="formData.birthM"
                                    :items="birthMList"
                                    :rules="selectRequired"
                                    disabled
                                    >
                            </v-select>
                        </v-col>
                        <v-col>
                            <v-select label="日"
                                    v-model="formData.birthD"
                                    :items="birthDList"
                                    :rules="selectRequired"
                                    disabled
                                    >
                            </v-select>
                        </v-col>
                    </v-row>
                    <!-- メールアドレス -->
                    <v-text-field label="メールアドレス"
                                    class="mt-3"
                                    v-model.lazy="formData.emailAddr"
                                    :rules="emailAddrRules"
                                    disabled
                                    >
                    </v-text-field>
                    <!-- 国籍 -->
                    <v-select label="国籍"
                                class=""
                                v-model="formData.citizenship"
                                :items="nationsList"
                                >
                    </v-select>
                    <!-- 郵便番号 -->
                    <v-text-field class=""
                                    label="郵便番号"
                                    v-model.lazy="formData.postcode"
                                    :rules="postcodeRules"
                                    >
                    </v-text-field>
                </v-form>

                <h3 color="red">
                    ((続きの質問などが入る))
                </h3>

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
            valid: false,
            birthYList: utils.yearsList(),
            birthMList: utils.monthsList,
            birthDList: utils.daysList,
            // 発症日, option
            onsetYList: utils.yearsList().filter((y)=>(/(202[012])/.test(y.value))),
            onsetMList: utils.monthsList,
            onsetDList: utils.daysList,
            nationsList: utils.nationsList,
            // Rules
            inputRequired: [utils.inputRequired],
            selectRequired: [utils.selectRequired],
            postcodeRules: [utils.postcodeCheck],
            emailAddrRules: [utils.emailAddrCheck],
            // form data
            formData: {},
        }
    },
    methods: {
        nextPage: function() {
            if (this.$refs.baseform.validate()) {
                this.$store.commit('updateFormData', this.formData)
                this.$router.push('/Step2Input02')
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
