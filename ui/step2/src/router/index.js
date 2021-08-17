import Vue from 'vue'
import VueRouter from 'vue-router'
import Entry from '@/Entry'
import Auth from '@/Auth'
import AuthError from '@/AuthError'
import Step2Input1 from '@/Step2Input1'
import Step2Input2 from '@/Step2Input2'
import Step2Input3 from '@/Step2Input3'
import Step2Input4 from '@/Step2Input4'
import InputDaily from '@/InputDaily'
import Step2Break from '@/Step2Break'
import End from '@/End'
import Error from '@/common/Error'
import NotFound from '@/common/NotFound'

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'Entry',
        component: Entry
    },
    {
        path: '/Auth',
        name: 'Auth',
        component: Auth
    },
    {
        path: '/AuthError',
        name: 'AuthError',
        component: AuthError
    },
    {
        path: '/Step2Input1',
        name: 'Step2Input1',
        component: Step2Input1
    },
    {
        path: '/Step2Input2',
        name: 'Step2Input2',
        component: Step2Input2
    },
    {
        path: '/Step2Input3',
        name: 'Step2Input3',
        component: Step2Input3
    },
    {
        path: '/Step2Input4',
        name: 'Step2Input4',
        component: Step2Input4
    },
    {
        path: '/InputDaily',
        name: 'InputDaily',
        component: InputDaily
    },
    {
        path: '/Step2Break',
        name: 'Step2Break',
        component: Step2Break
    },
    {
        path: '/End',
        name: 'End',
        component: End
    },
    {
        path: '/Error',
        name: 'Error',
        component: Error
    },
    {
        path: '/:pathMatch(.*)*',
        name: 'NotFound',
        component: NotFound
    },
]

const router = new VueRouter({
    //mode: 'history',
    mode: 'hash',
    routes
})

export default router
