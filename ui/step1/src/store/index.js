import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        formData: {},
        responseData: {},
        url: '',
    },
    mutations: {
        updateFormData(state, payload) {
            state.formData = payload
        },
        updateResponseData(state, payload) {
            state.responseData = payload
        }
    },
    actions: {
    },
    modules: {
    }
})
