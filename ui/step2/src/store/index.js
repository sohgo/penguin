import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        formData: {},
        responseData: {},
        activeDate: {}, // for DailyInput
    },
    mutations: {
        updateFormData(state, payload) {
            state.formData = Object.assign({}, state.formData, payload)
        },
        updateResponseData(state, payload) {
            state.responseData = payload
        },
        updateActiveDate(state, payload) {
            state.activeDate = payload
        }
    },
    actions: {
    },
    modules: {
    }
})
