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
                    お送りした認証コード<br>
                    （3組の4桁の数字）を<br>
                    入力して下さい。
                </h3>

                <v-form ref="baseform"
                        v-model="valid"
                        class="mx-3"
                        lazy-validation
                        >

                    <!-- メールアドレス -->
                    <v-text-field
                        label="メールアドレス"
                        class="mt-3"
                        v-model.lazy="formData.emailAddr"
                        :rules="emailAddrRules"
                        :disabled="givenEmailAddr"
                    ></v-text-field>

                    <!-- 認証コード -->
                    <v-row class="mt-3">
                        <v-col class="mt-3 mx-0">認証コード</v-col>
                    </v-row>
                    <v-row class="mx-1 mt-0 my-4"> 

                        <v-col class="pa-0 ma-0 accol">
                            <v-text-field
                                class="text-h6 acfield"
                                ref="ac1"
                                v-model.lazy="ac1"
                                :rules="acRequired"
                                placeholder="0000"
                                @input="ac1ScpecialInput()"
                                >
                            </v-text-field>
                        </v-col>
                        <span class="pa-0 mx-1 mt-3 acdash">―</span>
                        <v-col class="pa-0 ma-0 accol">
                            <v-text-field
                                class="text-h6 acfield"
                                ref="ac2"
                                v-model.lazy="ac2"
                                :rules="acRequired"
                                placeholder="0000"
                                >
                            </v-text-field>
                        </v-col>
                        <span class="pa-0 mx-1 mt-3 acdash">―</span>
                        <v-col class="pa-0 ma-0 accol">
                            <v-text-field
                                class="text-h6 acfield"
                                ref="ac3"
                                v-model.lazy="ac3"
                                :rules="acRequired"
                                placeholder="0000"
                                >
                            </v-text-field>
                        </v-col>
                    </v-row>

                </v-form>

                <v-btn
                    class="white--text pa-5"
                    color="#03AF7A"
                    @click="sendAuth"
                    block
                >
                    <h3>
                        送信する
                    </h3>
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
            givenEmailAddr: false,
            acRequired: [
                v => !!v || '認証コードは必須です。',
                v => /^\d{4}$/.test(v) || '4桁の数字を入力して下さい。'
            ],
            emailAddrRules: [utils.emailAddrCheck],
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
                utils.async_post(`${process.env.VUE_APP_SERVER_URL}/a`,
                    this.formData)
                    .then(ret => {
                        if (ret.code == 200) {
                            this.$store.state.authed = true
                            this.$store.state.formData = ret.data
                            this.$router.push('/input1')
                        } else if (ret.code == 406) {
                            this.$store.state.responseData = ret
                            this.$router.push('/autherror')
                        } else {
                            this.$store.state.responseData = ret
                            this.$router.push('/error')
                        }
                    })
            }
        },
        ac1ScpecialInput: function() {
            // if full authcode is inputed (e.g. copy&paste),
            // then split and put them.
            let value = this.ac1
            if (/^\d{4}-\d{4}-\d{4}$/.test(value)) {
                let vs = value.split('-')
                this.ac1 = vs[0]
                this.ac2 = vs[1]
                this.ac3 = vs[2]
            }
        }
    },
    watch: {
        ac1(v) { if (v.length >= 4) { this.$refs.ac2.focus() } },
        ac2(v) { if (v.length >= 4) { this.$refs.ac3.focus() } },
    },
    mounted: function() {
        this.formData = this.$store.state.formData
        // set the given email address if needed.
        let em = document.querySelector('meta[name="X-HKD-GIVEN-EM"]').getAttribute('content')
        if (em != "__HKD_GIVEN_EM__") {
            this.formData.emailAddr = em
            this.givenEmailAddr = true
        }
        // get xpath from the URL.
        let url = document.URL
        this.formData.xpath = url.substr(url.indexOf('/2/x/')+5, 64)
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
