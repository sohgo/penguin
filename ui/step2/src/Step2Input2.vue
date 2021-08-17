<template>
    <v-app>

        <v-app-bar color="#03AF7A" class="text-center"
                   elevation="0"
                   dense
                   app>
            <v-btn icon @click="movePage('/Step2Input1')">
                <v-icon class="white--text"
                    link
                >mdi-arrow-left</v-icon>
            </v-btn>
            <v-spacer></v-spacer>
            <v-app-bar-title class="white--text">
                入力２
            </v-app-bar-title>
            <v-spacer></v-spacer>
            <v-btn icon @click="movePage('/Step2Input3')">
                <v-icon class="white--text"
                    link
                >mdi-arrow-right</v-icon>
            </v-btn>
        </v-app-bar>

        <v-main>
            <div class="mx-3 my-5">
                <h1 class="my-3">
                    あなたの基礎疾患<br>
                    についてお伺いします。
                </h1>

                <p>
                    該当する疾患についてチェックしてください。
                </p>

                <v-form
                    class="ma-3"
                    ref="baseform"
                    v-model="valid"
                    lazy-validation
                >

                    <v-container
                        class="ma-0 pa-1"
                        v-for="(g, i) in sickList"
                        :key="i"
                    >
                        <v-row>
                            <v-checkbox
                                :label="g.label"
                                v-model="g.checked"
                                dense
                            >
                            </v-checkbox>
                        </v-row>
                        <template v-if="g.question && g.checked">
                            <v-row>
                                <v-textarea
                                    :label="g.question"
                                    rows="2"
                                    v-model="g.text"
                                    :disabled="!g.checked"
                                    :placeholder="g.checked ? g.placeholder : ''"
                                    dense
                                >
                                </v-textarea>
                            </v-row>
                        </template>
                    </v-container>

                </v-form>

                <v-btn
                    class="pa-5 white--text"
                    color="#03AF7A"
                    @click="movePage('/Step2Input3')"
                    block
                >
                    <span>
                        次へすすむ
                    </span>
                </v-btn>

            </div>
        </v-main>

    </v-app>
</template>

<script>
//import utils from '@/common/utils.js'

const healthProfile = [
    // 外部から入力
    {label:'該当しない',question:null,placeholder:'',error:''},
    {label:'妊娠',question:'妊娠何週目ですか？',placeholder:'',error:''},
    {label:'喫煙',question:'何歳から１日あたり何本吸いますか？',placeholder:'例) 20本',error:''},
    {label:'糖尿病',question:'具体的に教えてください',placeholder:'例)2型糖尿病でインスリン注射をしている。',error:''},
    {label:'呼吸器疾患（喘息・COPD・その他）',question:'具体的に教えてください',placeholder:'',error:''},
    {label:'腎疾患',question:'透析はしていますか？',placeholder:'',error:''},
    {label:'肝疾患',question:'具体的に教えてください',placeholder:'',error:''},
    {label:'心疾患',question:'具体的に教えてください',placeholder:'',error:''},
    {label:'神経筋疾患',question:'具体的に教えてください',placeholder:'',error:''},
    {label:'血液疾患（貧血等）',question:'具体的に教えてください',placeholder:'',error:''},
    {label:'免疫不全（HIV、免疫抑制剤使用含む）',question:'HIV、免疫抑制剤使用含む。具体的に教えてください。',placeholder:'',error:''},
    {label:'悪性腫瘍（がん）',question:'具体的に教えてください',placeholder:'',error:''},
    {label:'その他',question:'具体的に教えてください',placeholder:'',error:''},
    ]

export default {
    data() {
        return {
            valid: false,
            formData: {},
                /*
                ## formData.healthRecord
                - <LABEL>で一意になる健康状態のオブジェクト。
                - <LABEL>は healthProfile.labelから得る。
                    + healthProfileは外部から得る。
                - healthProfileに定義された全てのLABELを保持する。
                    + チェックした項目だけ保持すると、healthProfileが変更された時に、元の質問がわからなくなるため。
                - <TEXT>はGUIから入力される。前後の空白文字は削除する。
                - データモデル
                    + <TEXT> === null: チェックしていない。
                    + <TEXT> === '': チェックしている, 詳細なし。
                    + <TEXT> !== '': チェックしている。詳細あり。

                formData.healthRecord = {
                    <LABEL> : {
                        text: <TEXT>,
                    }, ...
                }
                */
            sickList: undefined, // healthRecordの作業用オブジェクト
        }
    },
    methods: {
        updateFormData: function() {
            // copy sickList back into formData.healthRecord
            // assuming that the all labels exist in formData.healthRecord.
            if (this.$refs.baseform.validate()) {
                for (let i = 0; i < this.sickList.length; i++) {
                    let v = this.sickList[i]
                    if (v.checked === true) {
                        this.formData.healthRecord[v.label] = {
                            text: v.text === null ? '' : v.text
                        }
                    } else {
                        this.formData.healthRecord[v.label] = {
                            text: null
                        }
                    }
                }
                // update formData
                this.$store.commit('updateFormData', this.formData)
            }
        },
        movePage: function(pageName) {
            if (this.$refs.baseform.validate()) {
                this.updateFormData()
                this.$router.push(pageName)
            }
        },
    },
    mounted: function() {
        this.formData = this.$store.state.formData
        if (this.formData.healthRecord === undefined) {
            /* initialize sickList */
            this.formData.healthRecord = {}
            this.sickList = healthProfile.map(v => {
                // add this label into formData.healthRecord here
                this.formData.healthRecord[v.label] = {
                    text: null
                }
                return Object.assign({}, v, {
                    checked: false,
                    text: null,
                })
            })
        } else {
            // this.formData.healthRecord !== undefined
            // copy formData.healthRecord into sickList.
            this.sickList = healthProfile.map(g => {
                let k = Object.keys(this.formData.healthRecord).filter(x => g.label == x)
                if (k.length == 1) {
                    // found the label in formData.healthRecord
                    let v = this.formData.healthRecord[k]
                    return Object.assign({}, g, {
                        checked: v.text !== null ? true : false,
                        text: v.text,
                    })
                } else if (k.length > 1) {
                    throw `ERROR: k.length = ${k.length}`
                } else {
                    // add this label into formData.healthRecord here
                    this.formData.healthRecord[g.label] = {
                        text: null
                    }
                    return Object.assign({}, g, {
                        checked: false,
                        text: null,
                    })
                }
            })
        }
    }
}
</script>

<style>
</style>
