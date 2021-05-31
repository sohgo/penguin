import Vue from 'vue'
import VueRouter from 'vue-router'
import Beginning from '@/Beginning'
import Step1Input from '@/Step1Input'
import Step1End from '@/Step1End'
import Error from '@/Error'
import NotFound from '@/NotFound'

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'Beginning',
        component: Beginning
    },
    {
        path: '/Step1Input',
        name: 'Step1Input',
        component: Step1Input
    },
    {
        path: '/Step1End',
        name: 'Step1End',
        component: Step1End
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
