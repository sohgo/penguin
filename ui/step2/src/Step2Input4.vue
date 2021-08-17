<template>
    <v-app>

        <v-app-bar color="#03AF7A" class="text-center"
                   elevation="0"
                   dense
                   app>
            <v-btn icon @click="movePage('/Step2Break')">
                <v-icon class="white--text"
                    link
                >mdi-arrow-left</v-icon>
            </v-btn>
            <v-spacer></v-spacer>
            <v-app-bar-title class="white--text">
                行動履歴
            </v-app-bar-title>
            <v-spacer></v-spacer>
            <v-btn icon disabled></v-btn>
        </v-app-bar>

        <v-main>
            <div class="mx-3 my-5">
                <h1 class="my-3">
                    過去２週間の行動を<br>入力してください。
                </h1>

                <v-btn
                    class="my-1"
                    v-for="(v, i) in getDateList()"
                    :key="i"
                    color=""
                    @click="goDailyInput(v.label)"
                    block
                >
                    <div class="mx-2 my-3">
                        <span style="font-size:130%">{{v.annotate}}</span> {{v.local}} {{v.dayWeek}}
                    </div>
                    <v-spacer>
                    </v-spacer>
                    <v-chip
                        :color="getDailyInputStatus(v.label, 'color')"
                        small
                    >
                        {{getDailyInputStatus(v.label, 'text')}}
                    </v-chip>
                </v-btn>

                <v-btn
                    class="white--text"
                    color="#03AF7A"
                    @click="movePage('/Step2End', true)"
                    block
                >
                    <h3>
                        保存して終了する。
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
            formData: null,
            /*
            ## formData.dailyActivities
            - 14日間の行動履歴
            - dateで一意になる。
            - 各メンバーの`detail.what !== undefined && detail.what.label !== undefined`の時、'入力済'と表示する。
                + '60%入力'などと表示するとなおいい。
            - データモデル

            formData.dailyActivities = [
                {
                    date: <YYYY-MM-DD>,
                    detail: [], // what,when,where,whomのリスト
                }, ...
            ]
            */
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
            // update formData
            this.$store.commit('updateFormData', this.formData)
        },
        movePage: function(pageName, doSubmit) {
            // validationは必要か？
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
        },
        getDateList: function() {
            if (this.formData === null) {
                return []
            } else {
                return utils.generatePastDateList(this.formData.onsetDate)
            }
        },
        goDailyInput: function(date) {
            this.$store.commit('updateActiveDate', date)
            this.$router.push('/InputDaily')
        },
        getDailyInputStatus: function(label, type) {
            let results = this.formData.dailyActivities.filter(g => g.date == label)
            if (results && results.length !== 1) {
                throw `ERROR: label ${label} が不正です。`
            }
            let da = results[0]
            // da.detail.length
            //     0: は1度も開いていない。
            //     1: は1度開いたが「何を」を登録していない。
            if (type == 'text') {
                if (da.detail.length > 1) {
                    return `${da.detail.length-1}件 登録済`
                } else {
                    return '未登録'
                }
            } else if (type == 'color') {
                if (da.detail.length > 1) {
                    return 'primary'
                } else {
                    return 'error'
                }
            } else {
                throw `ERROR: getDailyInputStatus type ${type} が不正です。`
            }
        },
    },
    mounted: function() {
        this.formData = this.$store.state.formData
        // set activities into activityList for reactivity.
        if (this.formData.dailyActivities == undefined) {
            this.formData.dailyActivities = this.getDateList().map(v=>({
                date: v.label,
                detail: []
            }))
        }
        console.log('formData', this.formData)
    }
}
</script>

<style>
</style>
