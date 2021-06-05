import Vue from 'vue'
import VueRouter from 'vue-router'
import Entry from '@/Entry'
import Auth from '@/Auth'
import AuthError from '@/AuthError'
import Step2Input from '@/Step2Input'
import Step2End from '@/Step2End'
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
        path: '/Step2Input',
        name: 'Step2Input',
        component: Step2Input
    },
    {
        path: '/Step2End',
        name: 'Step2End',
        component: Step2End
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
