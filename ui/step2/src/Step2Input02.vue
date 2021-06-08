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

                <h5 class="mx-3">
                    該当する疾患についてチェックしてください。
                </h5>
                <v-form ref="baseform"
                        v-model="valid"
                        class="ma-3"
                        lazy-validation
                        >

                    <v-container
                        v-for="v in input_sick"
                        :key="v.id"
                        class="pa-0 ma-0"
                        >
                        <v-row>
                            <v-checkbox :label="v.label"
                                    class=""
                                    v-model="v.c"
                                    dense
                                    >
                            </v-checkbox>
                        </v-row>
                        <template v-if="v.c">
                            <v-row>
                                <v-textarea :label="v.question"
                                        class=""
                                        rows="2"
                                        v-model="v.d"
                                        :disabled="!v.c"
                                        :placeholder="v.c ? v.placeholder : ''"
                                        dense
                                        >
                                </v-textarea>
                            </v-row>
                        </template>
                    </v-container>

                </v-form>

                <h3 color="red">
                    以降、続きの質問。。。
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
            valid: false,
            formData: {},
            input_sick: [
                {label:'妊娠',question:'妊娠何週目ですか？',required:'',placeholder:'',error:'',id:0,c:false,d:''},
                {label:'喫煙',question:'何歳から１日あたり何本吸いますか？',required:'',placeholder:'',error:'',id:1,c:false,d:''},
                {label:'糖尿病',question:'具体的に教えてください',required:'',placeholder:'例)2型糖尿病でインスリン注射をしている。',error:'',id:2,c:false,d:''},
                {label:'呼吸器疾患（喘息・COPD・その他）',question:'具体的に教えてください',required:'',placeholder:'',error:'',id:3,c:false,d:''},
                {label:'腎疾患',question:'透析はしていますか？',required:'',placeholder:'',error:'',id:4,c:false,d:''},
                {label:'肝疾患',question:'具体的に教えてください',required:'',placeholder:'',error:'',id:5,c:false,d:''},
                {label:'心疾患',question:'具体的に教えてください',required:'',placeholder:'',error:'',id:6,c:false,d:''},
                {label:'神経筋疾患',question:'具体的に教えてください',required:'',placeholder:'',error:'',id:7,c:false,d:''},
                {label:'血液疾患（貧血等）',question:'具体的に教えてください',required:'',placeholder:'',error:'',id:8,c:false,d:''},
                {label:'免疫不全（HIV、免疫抑制剤使用含む）',question:'HIV、免疫抑制剤使用含む。具体的に教えてください。',required:'',placeholder:'',error:'',id:9,c:false,d:''},
                {label:'悪性腫瘍（がん）',question:'具体的に教えてください',required:'',placeholder:'',error:'',id:10,c:false,d:''},
                {label:'その他',question:'具体的に教えてください',required:'',placeholder:'',error:'',id:11,c:false,d:''},
                ],
        }
    },
    methods: {
        submitData: async function() {
            if (this.$refs.baseform.validate()) {
                // copy input_sick into formData
                for (let i = 0; i < this.input_sick.length; i++) {
                    this.formData[`sick${i}_c`] = this.input_sick[i].c
                    this.formData[`sick${i}_d`] = this.input_sick[i].d
                }
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
