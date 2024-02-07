/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from '@/plugins'

// Components
import App from './App.vue'
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
import Home from '@/pages/Home.vue'
import Login from '@/pages/Login.vue'
import Register from '@/pages/Register.vue'
import Account from '@/pages/Account.vue'

// Composables
import { createApp } from 'vue'

import { createPinia } from 'pinia'

// Router
import {createRouter, createWebHistory} from 'vue-router'
import { useUserStore } from './stores/UserStore'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', name: 'Home', component: Home},
        { path: '/login', name: 'Login', component: Login},
        { path: '/register', name: 'Register', component: Register}
    ]
})

router.beforeEach(async (to) => {
    // redirect to login page if not logged in and trying to access a restricted page
    const publicPages = ['/login', '/register'];
    const authRequired = !publicPages.includes(to.path);
    const auth = useUserStore();

    if (authRequired && !auth.user) {
        auth.returnUrl = to.fullPath;
        return '/login';
    }
});

const pinia = createPinia()
const app = createApp(App)

app.use(pinia)
app.use(router)
registerPlugins(app)

app.mount('#app')
