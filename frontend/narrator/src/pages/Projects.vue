<template>
    <v-navigation-drawer>
        <v-list-item title="Narrator" subtitle="automatic data abstraction tool"></v-list-item>
        <v-divider></v-divider>
        <v-list-item link active title="projects"></v-list-item>
        <v-list-item link title="account settings"></v-list-item>
        <v-list-item link title="userguide"></v-list-item>
        <v-list-item link title="help?"></v-list-item>
        <v-spacer></v-spacer>
        <v-divider></v-divider>
        <v-list-item link title="logout" @click="logout"></v-list-item>
    </v-navigation-drawer>
    <!-- <Header></Header> -->
    <div class="projects">
        welcome to the home page,<b>--{{ userStore.user }}</b>
    </div>
    <Footer></Footer>
</template>

<script>
// 
import { useUserStore } from "@/stores/UserStore";
export default {
    setup() {
        const userStore = useUserStore();
        return { userStore };
    },

    data(){

    },

    methods:{
        async logout(){
            await this.userStore.logOut().then(() => {
                this.$router.push(this.$route.query.redirect || '/login');
            });
        }
    }

};
</script>


<style lang="scss">
.projects{
    color: #000;
    min-height: 93vh!important;
}
</style>