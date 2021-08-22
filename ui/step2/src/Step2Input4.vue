<template>
    <v-app>

        <v-app-bar color="#03AF7A" class="text-center"
                   elevation="0"
                   dense
                   app>
            <v-btn icon @click="movePage('/break')">
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
                    @click="movePage('/end', true)"
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

const cloneObject = (src) => {
    let dst, k, v
    // Object (except null) or others
    if (typeof src !== 'object' || src === null) {
        return src
    }
    // Array or others
    dst = Array.isArray(src) ? [] : {}
    for (k in src) {
        v = src[k]
        dst[k] = cloneObject(v)
    }
    return dst
}

export default {
    data() {
        return {
            valid: false,
            formData: null,
            /*
            ## formData.dailyActivities
            - 14日間の行動履歴
            - <YYYY-MM-DD>で一意になる。
            - 各メンバーの`what !== undefined && what.label !== undefined`の時、'入力済'と表示する。
                + '60%入力'などと表示するとなおいい。
            - データモデル

            formData.dailyActivities = {
                <YYYY-MM-DD> : [], // what,when,where,whomのリスト
            }
            */
            /*
            workData.dailyActivities = {
                <YYYY-MM-DD> : {
                    maxidx: 0,
                    detail: [], // what,when,where,whomのリスト
                }
            }
            */
        }
    },
    methods: {
        updateFormData: function() {
            // update formData
            let fda = this.formData.dailyActivities
            let wda = this.workData.dailyActivities
            for (let k in wda) {
                fda[k] = []
                for (let i = 0; i < wda[k].detail.length; i++) {
                    let dayAct = wda[k].detail[i]
                    if (dayAct.what.label === undefined) {
                        continue
                    }
                    // copy essential items in workData to formData.
                    let da = {}
                    da.what = {
                        label: dayAct.what.label,
                        text: dayAct.what.text,
                        selected: dayAct.what.selected,
                    }
                    da.when = {
                        label: dayAct.when.label,
                        timeFrom: dayAct.when.timeFrom,
                        timeTo: dayAct.when.timeTo,
                    }
                    da.where = {
                        text: dayAct.where.text,
                        address: dayAct.where.address,
                        serachKey: dayAct.where.serachKey,
                    }
                    da.whom = {
                        attendants: dayAct.whom.attendants,
                        numPeople: dayAct.whom.numPeople,
                        text: dayAct.whom.text,
                    }
                    da.comment = dayAct.comment
                    fda[k].push(da)
                }
            }
            //this.$store.commit('updateFormData', this.formData)
        },
        movePage: function(pageName, doSubmit) {
            // validationは必要か？
            this.updateFormData()
            if (doSubmit) {
                utils.async_post(`${process.env.VUE_APP_SERVER_URL}/2`,
                    JSON.parse(JSON.stringify(this.formData)))
                    .then(ret => {
                        if (ret.code == 200) {
                            this.$router.push(pageName)
                        } else {
                            this.$store.state.responseData = ret
                            this.$router.push('/error')
                        }
                    })
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
            this.$store.state.activeDate = date
            this.$router.push('/day')
        },
        getDailyInputStatus: function(label, type) {
            let ks = Object.keys(this.workData.dailyActivities).filter(k => k === label)
            if (ks.length !== 1) {
                throw `ERROR: label ${label} が不正です。`
            }
            let dayActsDetail = this.workData.dailyActivities[ks[0]].detail
            // workData.dailyActivities[k].detailのとりうる状態
            //     - [未入力]: 0件: 1度も開いていない。
            //     - [入力済]: 1件: 1度開いたが「何を」を登録していない。
            //     - [入力済,未入力]: 1件
            let num = dayActsDetail.filter(x => x.what && x.what.label !== undefined).length
            if (type == 'text') {
                if (num > 0) {
                    return `${num}件 登録済`
                } else {
                    return '未登録'
                }
            } else if (type == 'color') {
                if (num > 0) {
                    return 'primary'
                } else {
                    return 'error'
                }
            } else {
                throw `ERROR: getDailyInputStatus type ${type} が不正です。`
            }
        },
        newDayAct: function(da) {
            // copy formData.dailyActivities[k].detail into workData
            // See InputDaily.vue
            return {
                idx: 0, // updated later.
                opened: false,
                what: {
                    label: da.what.label,
                    text: da.what.text,
                    selected: da.what.selected,
                    tags: [], // changeWhatLabel()で初期化する。
                },
                when: {
                    label: da.when.label,
                    timeFrom: da.when.timeFrom,
                    timeTo: da.when.timeTo,
                    timeFromMenu: false,
                    timeToMenu: false,
                },
                where: {
                    text: da.where.text,
                    address: da.where.address,
                    searchKey: da.where.searchKey,
                    gmapDialogMenu: false,
                    gmo: null,  // google Map Object
                    gmg: null,  // google Map Geocode Object
                },
                whom: cloneObject(da.whom),
                comment: '',
            }
        },
    },
    mounted: function() {
        this.formData = this.$store.state.formData
        this.workData = this.$store.state.workData
        // initialize formData
        if (!this.formData.dailyActivities) {
            this.formData.dailyActivities = {}
        }
        // create workData.dailyActivities
        if (!this.workData.dailyActivities) {
            this.workData.dailyActivities = {}
            this.getDateList().forEach(v=>{
                this.workData.dailyActivities[v.label] = {
                    maxidx: 0, // updated later.
                    detail: [],
                }
            })
            let fda = this.formData.dailyActivities
            let wda = this.workData.dailyActivities
            for (let k in fda) {
                for (let i = 0; i < fda[k].length; i++) {
                    wda[k].detail.push(this.newDayAct(fda[k][i]))
                }
                wda[k].maxidx = wda[k].detail.length
            }
        }
    }
}
</script>

<style>
</style>
