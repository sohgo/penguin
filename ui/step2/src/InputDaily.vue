<template>
    <v-app>

        <v-app-bar color="#03AF7A" class="text-center"
                elevation="0"
                dense
                app
        >
            <v-btn icon @click="movePage('/Step2Input4')">
                <v-icon class="white--text"
                    link
                >mdi-arrow-left</v-icon>
            </v-btn>
            <v-spacer></v-spacer>
            <v-app-bar-title class="white--text">
                行動入力
            </v-app-bar-title>
            <v-spacer></v-spacer>
            <v-btn icon disabled></v-btn>
        </v-app-bar>

        <v-main>
            <div class="mx-3 my-5">
                <h1 class="my-3">
                    {{activeDate}}
                </h1>

                <p>この日の出来事・行動を教えてください。<br><br>
                ※各項目を選択すると詳細を記入できますので、わかる範囲で記載してください。<br>
                ※時系列は順不同で構いません。<br>
                ※「<v-icon dense>mdi-arrow-up-down-bold</v-icon>」をつまんで上下への並び替えが可能です。(未実装)</p>

                <v-form
                    class="ma-3"
                    ref="baseform"
                    v-model="valid"
                    lazy-validation
                >

                    <v-card class="my-2 pa-0"
                            v-for="dav in dailyActDetails"
                            :key="dav.idx"
                            :color="getCardColor(dav)"
                            >

                        <v-row class="ma-2">
                            <v-checkbox 
                                class="daily-input-title"
                                :on-icon="'mdi-chevron-down'"
                                :off-icon="'mdi-chevron-right'"
                                :label="getCardTitle(dav)"
                                v-model="dav.opened"
                                dense
                            >
                            </v-checkbox>
                            <v-spacer></v-spacer>
                            <v-btn class="mt-1" icon small>
                                <v-icon dense>
                                    mdi-arrow-up-down-bold
                                </v-icon>
                            </v-btn>
                        </v-row>

                        <template v-if="dav.opened">

                            <v-container v-if="!isDailyActReady(dav)">
                                <h4>最初に「何を」を選択して下さい。</h4>
                            </v-container>

                            <!-- なにを -->
                            <v-container>
                                <v-subheader class="daily-input-section white--text">「なにを」</v-subheader>
                                <v-select label="何をしましたか？"
                                        v-model="dav.what.label"
                                        :items="whatLabelList"
                                        @change="changeWhatLabel(dav)"
                                        >
                                </v-select>
                                <div v-if="isDailyActReady(dav)">
                                    <div>
                                        <span>行動</span>
                                        <v-btn v-for="(t, i) in dav.what.selected"
                                            :key="i"
                                            class="tag selected ma-2 pa-2"
                                            @click="removeTag(dav.what, i)"
                                            outlined
                                            x-small
                                        >
                                            <span>{{t}}</span>
                                            <v-icon right x-small>mdi-close-circle-outline</v-icon>
                                        </v-btn>
                                        <v-btn disabled icon></v-btn>
                                    </div>
                                    <v-divider></v-divider>
                                    <div>
                                        <div v-if="dav.what.tags.length">該当するものを選択(複数可)</div>
                                        <v-btn v-for="(t, i) in dav.what.tags"
                                            :key="i"
                                            class="tag suggested ma-2 pa-2"
                                            @click="addTag(dav.what, i)"
                                            outlined
                                            x-small
                                        >
                                            <span>{{t}}</span>
                                            <v-icon right>mdi-plus-circle-outline</v-icon>
                                        </v-btn>
                                    </div>
                                    <v-text-field
                                        label="具体的に詳しく教えてください。"
                                        v-model="dav.what.text"
                                        >
                                    </v-text-field>
                                </div>
                            </v-container>

                            <!-- いつ -->
                            <v-container v-if="isDailyActReady(dav)">
                                <v-card-subtitle class="daily-input-section pa-1 white--text">「いつ」</v-card-subtitle>
                                <div>いつ頃ですか？</div>
                                <v-radio-group
                                    v-model="dav.when.label"
                                    @change="changeWhenLabel(dav)"
                                >
                                    <v-radio class="px-4 ma-0"
                                            v-for="(d, i) in whenList"
                                            :key="i"
                                            :label="d.label"
                                            :value="d.label"
                                            >
                                    </v-radio>
                                </v-radio-group>
                                <div>時刻が分かれば入力して下さい。</div>
                                <v-menu
                                    :ref="`timeFromPicker${dav.idx}`"
                                    v-model="dav.when.timeFromMenu"
                                    :close-on-content-click="false"
                                    :nudge-right="40"
                                    :return-value.sync="dav.when.timeFrom"
                                    transition="scale-transition"
                                    offset-y
                                    max-width="290px"
                                    min-width="290px"
                                >
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-text-field
                                            v-model="dav.when.timeFrom"
                                            label="いつから"
                                            prepend-icon="mdi-clock-time-four-outline"
                                            readonly
                                            v-bind="attrs"
                                            v-on="on"
                                        ></v-text-field>
                                    </template>
                                    <v-time-picker
                                        v-if="dav.when.timeFromMenu"
                                        :allowed-minutes="m => m%5==0"
                                        v-model="dav.when.timeFrom"
                                        full-width
                                        @click:minute="$refs[`timeFromPicker${dav.idx}`][0].save(dav.when.timeFrom)"
                                    ></v-time-picker>
                                </v-menu>
                                <v-menu
                                    :ref="`timeToPicker${dav.idx}`"
                                    v-model="dav.when.timeToMenu"
                                    :close-on-content-click="false"
                                    :nudge-right="40"
                                    :return-value.sync="dav.when.timeTo"
                                    transition="scale-transition"
                                    offset-y
                                    max-width="290px"
                                    min-width="290px"
                                >
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-text-field
                                            v-model="dav.when.timeTo"
                                            label="いつまで"
                                            prepend-icon="mdi-clock-time-four-outline"
                                            readonly
                                            v-bind="attrs"
                                            v-on="on"
                                        ></v-text-field>
                                    </template>
                                    <v-time-picker
                                        v-if="dav.when.timeToMenu"
                                        :allowed-minutes="m => m%5==0"
                                        v-model="dav.when.timeTo"
                                        full-width
                                        @click:minute="$refs[`timeToPicker${dav.idx}`][0].save(dav.when.timeTo)"
                                    ></v-time-picker>
                                </v-menu>
                            </v-container>

                            <!-- どこで -->
                            <v-container v-if="isDailyActReady(dav)">
                                <v-subheader class="daily-input-section white--text">「どこで」</v-subheader>
                                <v-text-field
                                    v-model="dav.where.text"
                                    label="施設名・場所名を教えてください。"
                                    placeholder="例) スターバックス〇〇店、イオンモール〇〇店のフードコート"
                                >
                                </v-text-field>
                                <v-text-field
                                    v-model="dav.where.address"
                                    label="住所を教えて下さい。(地図から検索できます。)"
                                    placeholder="分かる範囲でお願いします。"
                                >
                                </v-text-field>

<!-- google map -->
                <v-dialog
                    v-model="dav.where.gmapDialogMenu"
                    persistent
                    max-width="600px"
                >
                    <template v-slot:activator="{ on, attrs }">
                        <v-btn
                            color="primary"
                            dark
                            v-bind="attrs"
                            v-on="on"
                            @click="gmapLoad(dav)"
                        >
                            地図から選択
                        </v-btn>
                    </template>
                    <v-card>
                        <v-card-title>
                            <span class="text-h5">中央の{{gmapCenterAimChar}}に場所を合わせて<br>選択して下さい。</span>
                        </v-card-title>

                        <v-card-text>
                            <v-row>
                                <v-text-field
                                    v-model="dav.where.searchKey"
                                    label="施設名や住所などで検索"
                                    placeholder="例) 北海道庁、札幌市〇〇スーパー"
                                >
                                </v-text-field>
                                    <v-btn
                                        color="primary"
                                        @click="startSearch(dav)"
                                    >
                                        検索
                                    </v-btn>
                            </v-row>
                            <v-row>
                                <div class="gmap" :ref="`gmap${dav.idx}`">
                                <!-- ここにgoogle mapが表示される -->
                                </div>
                            </v-row>
                        </v-card-text>

                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn
                                color="error"
                                @click="closeDialog(false, dav)"
                            >
                                キャンセル
                            </v-btn>
                            <v-btn
                                color="success"
                                @click="closeDialog(true, dav)"
                            >
                                この場所で決定
                            </v-btn>
                        </v-card-actions>
                    </v-card>
                </v-dialog>
<!-- google map -->

                            </v-container>

                            <!-- だれと -->
                            <v-container v-if="isDailyActReady(dav)">
                                <v-subheader class="daily-input-section white--text">「だれと」</v-subheader>
                                <div>「だれ」と一緒にいたか教えてください。</div>
                                <v-container>
                                    <v-checkbox v-for="(g, i) in dav.whom.attendants"
                                        :label="g.label"
                                        :key="i"
                                        v-model="g.checked"
                                        dense
                                    >
                                    </v-checkbox>
                                </v-container>
                                <v-divider></v-divider>
                                <div>周りに何人くらいいたか教えて下さい。</div>
                                <v-container>
                                    <v-radio-group
                                        v-model="dav.whom.numPeople"
                                    >
                                        <v-radio class="px-4 ma-0"
                                                v-for="(d, i) in numPeopleList"
                                                :key="i"
                                                :label="d"
                                                :value="d"
                                                >
                                        </v-radio>
                                    </v-radio-group>
                                </v-container>
                                <v-text-field
                                    label="その他気づいたことを教えて下さい。"
                                    v-model="dav.what.text"
                                    >
                                </v-text-field>
                            </v-container>

                            <v-card-actions>
                                <v-spacer/>
                                <v-btn
                                    @click="removeDailyAct(dav.idx)"
                                    outlined
                                    color="red lighten-1"
                                    class="mb-3">
                                    削除
                                </v-btn>
                            </v-card-actions>

                        </template>

                    </v-card>

                </v-form>

                <v-divider></v-divider>

                <v-container class="ma-4">
                    <v-row justify="center">
                        <v-btn
                            class="pa-5 white--text error"
                            @click="movePage('/Step2Input4', false)"
                        >
                            <span>
                                破棄する
                            </span>
                        </v-btn>
                        <v-btn
                            class="pa-5 white--text"
                            color="#03AF7A"
                            @click="movePage('/Step2Input4')"
                        >
                            <span>
                                保存する
                            </span>
                        </v-btn>
                    </v-row>
                </v-container>

            </div>
        </v-main>

    </v-app>
</template>

<script>

//import utils from '@/common/utils.js'

const gmapCenterAimChar = '✛'
const gmapInitZoomValue = 14

const googleMapOptions = {
    center: {
        lat: 43.0643091,
        lng: 141.3468324,
    },
    zoom: gmapInitZoomValue,
    //maxZoom: 15,
    minZoom: 3,
    zoomControl: true,
    mapTypeControl: false,
    scaleControl: false,
    streetViewControl: false,
    rotateControl: false,
    fullscreenControl: false,
}

const whatList = [
    // 外部から取得する。変更禁止。
    {label: '食事', tags: ['自宅で食べた', '外食']},
    {label: '移動・通勤・通学', tags: ['徒歩', '電車', 'バス', '自家用車', '自転車']},
    {label: '仕事・学業', tags: ['学校に通った', '自宅でリモート', '会社に通勤した', '屋外作業があった', 'アルバイト', '内職', '自家営業手伝い']},
    {label: '家事', tags: ['料理', '掃除・洗濯']},
    {label: '介護・看護・育児', tags: ['家族の介護・看護・育児', '介護サービスによる入浴']},
    {label: '買い物', tags: ['食料品・日用品', '電化製品・レジャー製品', 'ビデオなどのレンタル', 'ネットショッピング']},
    {label: '身の回りの用事', tags: ['入浴', '身じたく・着替え', '理美容室でのカット・パーマ', 'マッサージ・エステ']},
    {label: '趣味・娯楽', tags: ['映画', '博物館・美術館', '水族館・遊園地', 'スポーツ鑑賞', '楽器演奏', '手芸・華道', 'ガーデニング', 'ペット等の飼育', 'ドライブ', '読書・ゲーム', 'お菓子作り']},
    {label: 'スポーツ', tags: ['ジョギング・ランニング', '水泳', '球技', 'クラブ・サークル活動']},
    {label: '社会的活動', tags: ['施設や公園などの清掃', '植栽ボランティア', '交通安全見守り', '美術館ガイド', '労働組合運動', '布教活動', '献血', '民生委員', '施設の慰問']},
    {label: '交際・付き合い', tags: ['訪問・来客の接待や会話', '冠婚葬祭', '歓迎会・送別会・同窓会などの会合']},
    {label: '受診・療養', tags: ['病院での受診・治療', '健康診断']},
    {label: '旅行・行楽', tags: ['求職活動', 'お墓参り']},
    {label: 'その他', tags: []},
    ]

const whenList = [
    // 気象庁, https://www.jma.go.jp/jma/kishou/know/yougo_hp/toki.html
    // 終日を除く
    {label: '終日', timeFrom: '00:00', timeTo: '24:00' },
    {label: '未明', timeFrom: '00:00', timeTo: '03:00' },
    {label: '明け方', timeFrom: '03:00', timeTo: '06:00' },
    {label: '朝', timeFrom: '06:00', timeTo: '09:00' },
    {label: '午前', timeFrom: '00:00', timeTo: '12:00' },
    {label: '昼前', timeFrom: '09:00', timeTo: '12:00' },
    {label: '昼頃', timeFrom: '11:30', timeTo: '13:30' },
    {label: '昼過ぎ', timeFrom: '12:00', timeTo: '15:00' },
    {label: '午後', timeFrom: '12:00', timeTo: '24:00' },
    {label: '夕方', timeFrom: '15:00', timeTo: '18:00' },
    {label: '夜', timeFrom: '18:00', timeTo: '21:00' },
    {label: '深夜', timeFrom: '21:00', timeTo: '24:00' },
    {label: 'わからない', timeFrom: '', timeTo: '' },
    ]

const whomList = [
    '1人だった',
    '家族',
    '友人',
    '恋人',
    '同僚',
    'その他',
    ]

const numPeopleList = [
    '2～5名',
    '5名～10名',
    '10名以上',
    ]

export default {
    data: () => ({
        // form data
        valid: false,
        idx: 0, // identifier for refs.
        formData: {},
        dailyAct: null, // formData.dailyActivity[n] へのポインタ
            /*
            ## formData.dailyActivity[n]
            - その日の行動を記録したwhat,when,where,whomのリスト
            - データモデル

            formData.dailyActivity[n] = {
                date: <YYYY-MM-DD>,
                detail: [
                    {
                        opened: false, // true: 開く。false: 閉じる。
                        // what === undefinedなら、タイトルに'クリックして入力'を表示。
                        // それ以外なら、
                        // what.label, when.label, where.tags の順でいずれか1つを表示。
                        what: {
                            label: '<LABEL>', // whatList.label
                            text: '<自由記述>', // 何をしていたか
                            selected: [],
                            tags: [ '<TAG>', ... ], // whatList.tags, formDataへコピーしない。
                        },
                        when: {
                            label: '<WHEN>', // whenList.label
                            timeFrom: 'HH:MM', // whenList.fimrFrom
                            timeTo: 'HH:MM', // whenList.fimrTo
                        },
                        where: {
                            text: '<自由記述>', // 施設名、何階、部屋名など
                            address: '<自由記述>', // 住所、google mapから入力可能
                            // textからsearchKeyに初期入力できていると最高
                            searchKey: '', // gmapから入力された検索キー
                            // 以下は候補がいくつかある場合に選択させる場合。
                            // tags: [ <TAG>, ... ],
                            // whereList: [ 'label', ...], // whereList.label, formDataへコピーしない。
                        },
                        whom: {
                            attendants: [ <TAG>, ... ], // 誰と, checkbox
                            numPeople: <TAG>, // 何名くらい, radio button
                            text: '<自由記述>'
                        },
                        comment: '<自由記述>'
                    }, ...
                ]
            }
            */

        /* google map */
        lat: null,
        lng: null,
        timerCheckGmapElm: null,
        latlngSearched: null,
    }),
    computed: {
        dailyActDetails: function() {
            if (this.dailyAct === null) {
                return []
            } else {
                return this.dailyAct.detail
            }
        },
        activeDate: function() {    // XXX propsに置き換えるべき
            return this.$store.state.activeDate
        },
        whatLabelList: function() {
            return whatList.map(v=>v.label)
        },
        whenList: function() {
            return whenList
        },
        numPeopleList: function() {
            return numPeopleList
        },
        gmapCenterAimChar: function() {
            return gmapCenterAimChar
        },
    },
    methods: {
        updateFormData: function() {
            if (this.$refs.baseform.validate()) {
                // XXX more work
                // update formData
                this.$store.commit('updateFormData', this.formData)
                return true
            } else {
                this.check_validity(this.$refs.baseform.$children)
                return false
            }
        },
        check_validity: function(children) {
            for (let i = 0; i < children.length; i++) {
                if (children[i].valid === false) {
                    children[i].focus()
                } else if (children[i].valid === undefined) {
                    this.check_validity(children[i].$children)
                }
            }
        },
        movePage: function(pageName, doSave) {
            if (doSave) {
                if (this.$refs.baseform.validate()) {
                    if (this.updateFormData()) {
                        this.$router.push(pageName)
                    }
                }
            } else {
                this.$router.push(pageName)
            }
        },
        isDailyActReady: function(dav) {
            return dav.what.label !== undefined
        },
        getCardColor: function(dav) {
            return this.isDailyActReady(dav) ? 'green lighten-5' : 'red lighten-5'
        },
        getCardTitle: function(dav) {
            return this.isDailyActReady(dav) ? dav.what.label : 'クリックして入力'
        },
        hasDailyActNewEntry: function() {
            for (let i = 0; i < this.dailyAct.detail.length; i++) {
                if (this.dailyAct.detail[i].what.label === undefined) {
                    return true
                }
            }
            return false
        },
        addDailyActDefault: function() {
            this.idx += 1
            this.dailyAct.detail.push({
                idx: this.idx,
                opened: false,
                what: {
                    label: undefined,
                    text: '',
                    tags: [], // changeWhatLabel()で初期化する。
                    selected: [],
                },
                when: {
                    label: undefined,
                    timeFrom: '',
                    timeTo: '',
                    timeFromMenu: false,
                    timeToMenu: false,
                },
                where: {
                    text: '',
                    address: '',
                    searchKey: '',
                    gmapDialogMenu: false,
                    gmo: null,  // google Map Object
                    gmg: null,  // google Map Geocode Object
                },
                whom: {
                    attendants: whomList.map(v=>({
                        label: v,
                        checked: false,
                    })),
                    numPeople: '',
                    text: '',
                }
            })
        },
        removeDailyAct: function(idx) {
            this.dailyAct.detail.splice(idx, 1)
            if (!this.hasDailyActNewEntry()) {
                this.addDailyActDefault()
            }
        },
        changeWhatLabel: function(dav) {
            dav.what.tags = whatList.filter(v=> v.label == dav.what.label)[0].tags
            // 新規入力用エントリがなければ追加する。
            if (!this.hasDailyActNewEntry()) {
                this.addDailyActDefault()
            }
        },
        addTag: function(obj, idx) {
            obj.selected = obj.selected.concat(obj.tags.splice(idx,1)).sort()
        },
        removeTag: function(obj, idx) {
            obj.tags = obj.tags.concat(obj.selected.splice(idx,1)).sort()
        },
        changeWhenLabel: function(dav) {
            let w = whenList.filter(v=> v.label == dav.when.label)[0]
            dav.when.timeFrom = w.timeFrom
            dav.when.timeTo = w.timeTo
        },
        /* google map */
        removePrefixJapan: function(str) {
            const prefix = '日本、'
            if (str.indexOf(prefix) === 0) {
                return str.slice(prefix.length)
            } else {
                return str
            }
        },
        getGeocode: async function(dav, request) {
            if (dav.where.gmg === null) {
                dav.where.gmg = new window.google.maps.Geocoder()
            }
            console.log('geocode request', request)
            return await dav.where.gmg.geocode(request)
                .then(({ results }) => {
                    console.log('#restuls', results.length)
                    // results[0]がもっともらしい結果。
                    return results[0]
                })
                .catch(e => {
                    window.alert("Geocodingに失敗しました。" + e)
                    return null
                })
        },
        startSearch: function(dav) {
            if (!dav.where.searchKey) {
                window.alert("検索キーワードを入力して下さい。")
                return false
            }
            // initialize
            const request = {
                query: dav.where.searchKey,
                fields: [
                    "name",
                    "formatted_address",
                    "geometry",
                ]}
            // start searching
            let service = new window.google.maps.places.PlacesService(dav.where.gmo)
            service.findPlaceFromQuery(request, (results, status) =>
                {
                    console.log("status", status)
                    if (status === window.google.maps.places.PlacesServiceStatus.OK) {
                        // Status.OK で !results という状況はあるだろうか？
                        if (results) {
                            console.log("#results", results.length)
                            // findPlaceFromQuery()は常にresults[0]を採用する。
                            let result = results[0]
                            dav.where.gmo.setCenter(result.geometry.location)
                            dav.where.gmo.setZoom(gmapInitZoomValue)
                            // PlaceResultにマーカーを置く。
                            let marker = new window.google.maps.Marker({ map: dav.where.gmo })
                            marker.setPosition(result.geometry.location)
                            this.setCoordinateSearched(result)
                            // address表示に"日本、"と入るので削除する。
                            dav.where.address = this.removePrefixJapan(result.formatted_address)
                        } else {
                            window.alert('検索に失敗しました。' +
                                'but, status was OK')
                        }
                    } else {
                        window.alert('検索に失敗しました。 ' + status)
                    }
                }
            )
        },
        roundLatLng: function(latlng /* LatLng Object */) {
            // 小数点7桁を切り捨てて保存する。
            // dragしていなかったらsearchしないようにするため。
            // そのまま比較すると以下の様な状況になる。
            //     lat 43.0643091 != 43.06430910000006
            // getCenter()の戻り値がやりすぎてる？
            let digit = 1000000
            return {
                lat: Math.round(latlng.lat() * digit) / digit,
                lng: Math.round(latlng.lng() * digit) / digit
            }
        },
        setCoordinateSearched: function(result) {
            let latlng = this.roundLatLng(result.geometry.location)
            // store the coordinate of this search.
            this.latlngSearched = latlng
            this.lat = latlng.lat
            this.lng = latlng.lng
        },
        setCoordinateCenter: function(dav) {
            let latlng = this.roundLatLng(dav.where.gmo.getCenter())
            this.lat = latlng.lat
            this.lng = latlng.lng
        },
        closeDialog: function(takeAddress, dav) {
            // takeAddress === false, do noting, just close the dialog.
            if (takeAddress) {
                this.setCoordinateCenter(dav) // for sure.
                // centerのgeocodeから住所を検索する。
                //   + 検索されていない
                //   + centerが変更されている
                if (!this.latlngSearch ||
                    (this.latlngSearched.lat != this.lat ||
                     this.latlngSearched.lng != this.lng)) {
                    this.getGeocode(dav, { location: dav.where.gmo.getCenter() })
                        .then(ret => {
                            console.log('getGeocode result', ret)
                            dav.where.address = this.removePrefixJapan(ret.formatted_address)
                            this.setCoordinateSearched(ret)

                            console.log('address', dav.where.address)
                            console.log('searchKey', dav.where.searchKey)
                            console.log('lat, lng:', this.lat, this.lng)
                        })
                }
            }
            dav.where.gmapDialogMenu = false
            clearInterval(this.timerCheckGmapElm)
        },
        gmapLoad: function(dav) {
            let self = this // callback内でthisが置き換わるので保存する。
            let initSearchKey = dav.where.text
            let elmRef = `gmap${dav.idx}`
            console.log('refs=', elmRef, self.$refs)
            //
            function gmapInit(gmapRef, dragCallback) {
                async function initmap() {
                    return await new window.google.maps.Map(gmapRef, googleMapOptions)
                }
                initmap()
                    .then(ret => {
                        dav.where.gmo = ret
                        console.log('gmo', dav.where.gmo)
                        window.google.maps.event.addListener(
                            dav.where.gmo,
                            'dragend',
                            dragCallback)
                    })
                    .catch(err => {console.log(err)})
            }
            function dragCallback() {
                self.setCoordinateCenter(dav)
            }

            self.timerCheckGmapElm = setInterval(() => {
                let gmapRef = self.$refs[elmRef][0]
                if (gmapRef) {
                    console.log('dialog loaded', elmRef, gmapRef)
                    clearInterval(self.timerCheckGmapElm)
                    if (dav.where.gmo === null) {
                        gmapInit(gmapRef, dragCallback)
                        gmapRef.insertAdjacentHTML('beforeend',
                            `<div class="gmap-aim">${gmapCenterAimChar}</div>`
                        )
                        if (initSearchKey) {
                            dav.where.searchKey = initSearchKey
                            self.startSearch(dav)
                        }
                    }
                }
            }, 500)
        }
    },
    mounted: function() {
        let self = this
        function initNext(self) {
            self.formData = self.$store.state.formData
            self.dailyAct = self.formData.dailyActivities.filter(v=> v.date == self.activeDate)[0]
            if (self.dailyAct.detail.length === 0) {
                // set activities into activityList for reactivity.
                self.addDailyActDefault()
            }
        }
        let baseurl = 'https://maps.googleapis.com/maps/api/js?language=ja&region=JP&libraries=places&callback=window.gmapGlobalInit'
        let apikey = 'APIKEY'
        if (!window.gmapGlobalInit) {
            window.gmapGlobalInit = () => {
                window.gmapGlobalLoaded = true
                console.log('Google Maps API ready', window.google)
                initNext(self)
            }
        } else {
                initNext(self)
        }
        if (!window.gmapGlobalLoaded) {
            let script = document.createElement('script');
            script.src = `${baseurl}&key=${apikey}`
            script.async = true
            script.defer = true
            document.head.appendChild(script);
        }
    }
}
</script>

<style>
.gmap {
    width: 505px;
    height: 505px;
    margin: 0 auto;
    background:transparent;    
}
.gmap-aim {
    z-index: 999;
    margin: 0;
    position: absolute;
    top: 50%;
    left: 50%;
    -ms-transform: translate(-50%, -50%);
    transform: translate(-50%, -50%);
    color: red;
    opacity: 0.7;
    font-size: x-large;
}
</style>

