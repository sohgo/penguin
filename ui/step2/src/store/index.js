import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        formData: {},   // data to be submitted.
        authed: false,
        workData: {},
        responseData: {},
        activeDate: {}, // for DailyInput
    },
    mutations: {
        /*
        updateFormData(state, payload) {
            state.formData = Object.assign({}, state.formData, payload)
        },
        */
        /*
        createSubmitData(state) {
            state.submitData = JSON.parse(JSON.stringify(state.formData))
        },
        */
    },
    actions: {
    },
    getters : {
        isAuthed: state => !!state.authed,
    },
    modules: {
    }
})
