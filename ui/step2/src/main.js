import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import router from './router'
import store from './store'

Vue.config.productionTip = false

new Vue({
    vuetify,
    router,
    store,
    render: h => h(App),
    created() {
        // push a history.
        console.log('url', window.location.href)
        let url = window.location.href
        let a = url.indexOf('/2/x/')
        let b = url.indexOf('?em=')
        if (a > -1) {
            if (b > -1) {
                url = url.substr(a, b-a)
            } else {
                url = url.href.substr(a)
            }
        }
        window.history.pushState({}, '新型コロナの調査', url)
        //
        if (process.env.NODE_ENV != 'development') {
            if (this.$state && this.$state.formData && this.$state.formData.onsetDate) {
                window.onbeforeunload = function (e) {
                    e = e || window.event
                    //for old browsers
                    if (e) {e.returnValue = 'Changes you made may not be saved';}
                    //for safari, chrome(chrome ignores text)
                    return 'Changes you made may not be saved';
                };
                if (performance.getEntriesByType("navigation")[0]['type'] == 'reload') {
                    this.$router.push('/Step2Input1')
                }
            }
        }
        // XXX DEBUG ONLY, TO BE REMOVED
        if (process.env.NODE_ENV == 'development') {
            this.$store.state.formData.emailAddr = 'test@example.org'
            this.$store.state.formData.onsetDate = '2021-08-01'
        }
        // XXX DEBUG ONLY, TO BE REMOVED
    }
}).$mount('#app')
