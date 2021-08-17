<template>
    <v-app>

        <v-app-bar color="#03AF7A" class="text-center"
            elevation="0"
            dense
            app
        >
            <v-btn icon @click="movePage('/Step2Input2')">
                <v-icon class="white--text"
                    link
                >mdi-arrow-left</v-icon>
            </v-btn>
            <v-spacer></v-spacer>
            <v-app-bar-title class="white--text">
                入力３
            </v-app-bar-title>
            <v-spacer></v-spacer>
            <!-- ここは将来的にはdisableにする。 -->
            <v-btn icon @click="movePage('/Step2Break')">
                <v-icon class="white--text"
                    link
                >mdi-arrow-right</v-icon>
            </v-btn>
        </v-app-bar>

        <v-main>
            <div class="mx-3 my-5">
                <h1 class="my-3">
                    <ruby>過去<rt>かこ</rt></ruby>14日<ruby>以内<rt>いない</rt></ruby>に<ruby>下記<rt>かき</rt></ruby>の<ruby>場所<rt>ばしょ</rt></ruby>を<br>
                    <ruby>訪<rt>おと</rt></ruby>れたことがありますか？
                </h1>

                <p>
                    <ruby>
                    該当<rt>がいとう</rt></ruby>
                    する
                    <ruby>
                    日付<rt>ひづけ</rt></ruby>
                    にチェックしてください。
                </p>

                <v-form
                    class="ma-3"
                    ref="baseform"
                    v-model="valid"
                    lazy-validation
                >

                    <v-container
                        class="ma-0 pa-1"
                        v-for="(v, i) in input_presence"
                        :key="i"
                    >
                        <v-row>
                            <v-checkbox
                                :label="v.label"
                                v-model="v.checked"
                                dense
                            >
                            </v-checkbox>
                        </v-row>
                        <template v-if="v.checked">
                            <p>いつ訪れましたか？</p>
                            <v-checkbox
                                class="ma-0 pa-0"
                                v-for="(d, i) in v.dateList"
                                :key="i"
                                :label="d.label"
                                v-model="d.checked"
                                dense
                                >
                            </v-checkbox>
                        </template>
                    </v-container>

                </v-form>

                <v-btn
                    class="white--text"
                    color="#03AF7A"
                    @click="movePage('/Step2Break', true)"
                    block
                >
                    <h3>
                        登録して次へすすむ
                    </h3>
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
            input_presence: [
/*
入力している日付が、クラスター認定日(YYYY-MM-DD)よりも後60日(要確認)ならば表示する。とかする？
formData = {
    onsetDate: <YYYY-MM-DD>,
    presenceData: {
        '<label>': [ false, true, ..., false ] // 14日分, 0, -1, -2, ..., -13
        ,...
    }
}

dateList = [ { label: <LABEL>, checked: <BOOL> }, ... ]
*/
// 名称,エリア,クラスター認定日,住所
// XXX 外部から読み込めるようにする。
{ label: '北翔第九病院', area: '石狩', date: '2021-08-04', address: '北海道〇△市〇△□〇△□〇△□〇△□〇△□〇△□', checked:null, dateList:null },
{ label: '養護老人ホームはるか豊潤', area: '胆振', date: '2021-08-09', address: '北海道〇△市〇△□〇△□〇△□〇△□〇△□〇△□', checked:null, dateList:null },
{ label: 'しつげんタクシー', area: '釧路', date: '2021-08-14', address: '北海道〇△市〇△□〇△□〇△□〇△□〇△□〇△□', checked:null, dateList:null },
{ label: '栗田病院', area: '胆振', date: '2021-08-21', address: '北海道〇△市〇△□〇△□〇△□〇△□〇△□〇△□', checked:null, dateList:null },
{ label: '後志総合協会病院', area: '後志', date: '2021-08-24', address: '北海道〇△市〇△□〇△□〇△□〇△□〇△□〇△□', checked:null, dateList:null },
{ label: '緑川新高校', area: '石狩', date: '2021-08-29', address: '北海道〇△市〇△□〇△□〇△□〇△□〇△□〇△□', checked:null, dateList:null },
{ label: '手稲総合病院', area: '石狩', date: '2021-09-03', address: '北海道〇△市〇△□〇△□〇△□〇△□〇△□〇△□', checked:null, dateList:null },
                ],
        }
    },
    methods: {
        submitData: async function() {
            // TO BE MERGED, duplicate definitions.
            // assuming that updateFormData() has been called.
            // try to submit data
            let url = `${process.env.VUE_APP_SERVER_URL}/2`
            let response = await utils.async_post(url, this.$store.state.formData)
            if (response.code == 200) {
                return true
            } else {
                return false
            }
        },
        updateFormData: function() {
            if (this.$refs.baseform.validate()) {
                // copy input_presence back into formData
                for (let i = 0; i < this.input_presence.length; i++) {
                    let node = this.input_presence[i]
                    if (node.checked === true) {
                        this.formData.presenceData[node.label] = node.dateList.map((x) => x.checked)
                    } else {
                        delete(this.formData.presenceData[this.input_presence[i].label])
                    }
                }
                // update formData
                this.$store.commit('updateFormData', this.formData)
            }
        },
        movePage: function(pageName, doSubmit) {
            if (this.$refs.baseform.validate()) {
                this.updateFormData()
                if (doSubmit) {
                    let response = this.submitData()
                    if (response) {
                        this.$router.push(pageName)
                    } else {
                        // エラーの場合、responseを保存する。要考察。
                        this.$store.commit('updateResponseData', response)
                        this.$router.push('/Error')
                    }
                } else {
                    this.$router.push(pageName)
                }
            }
        },
    },
    mounted: function() {
        this.formData = this.$store.state.formData
        /* initialize presenceData and input_presence */
        if (this.formData.presenceData === undefined) {
            this.formData.presenceData = {}
        }
        for (let i = 0; i < this.input_presence.length; i++) {
            let placename = this.input_presence[i].label
            this.input_presence[i].checked = this.formData.presenceData[placename] === undefined ? false : true
            this.input_presence[i].dateList = utils.generatePastDateList(this.formData.onsetDate).map((v,j) => ({
                label: `${v.local} ${v.annotate}`,
                checked: this.formData.presenceData[placename] === undefined ? false : this.formData.presenceData[placename][j]
            }))
        }
    },
}
</script>

<style>
</style>
