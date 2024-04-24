import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'

loadFonts()

// Plugins
import { registerPlugins } from '@/plugins'


// Layouts
import AuthLayout from '@/pages/auth/partials/AuthLayout.vue'

// Components
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
import Projects from '@/pages/Projects.vue'
import Login from '@/pages/auth/Login.vue'
import Register from '@/pages/auth/Register.vue'
import Account from '@/pages/Account.vue'
import ProjectItem from '@/components/ProjectItem.vue'
import ProjectDetails from '@/pages/ProjectDetails.vue'

// Composables

import { createPinia } from 'pinia'

// Router
import {createRouter, createWebHistory} from 'vue-router';
import { useUserStore } from './stores/UserStore';
import { useProjectStore } from './stores/ProjectStore';


const router = createRouter({
    history: createWebHistory(),
    routes: [
        { name: 'projects', path: '/projects', component: Projects},
        { name: 'project_details', path: '/projects/:id', component: ProjectDetails},
        { name: 'login', path: '/login', component: Login},
        { name: 'register', path: '/register', component: Register}
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
app.use(vuetify)

registerPlugins(app)

app.component('AuthLayout', AuthLayout)
app.component('Header', Header)

app.mount('#app')