<template>
    <v-layout>
        <v-navigation-drawer>
            <v-list-item title="ADA_T" subtitle="Automatic Data Abstraction Tool"></v-list-item>
            <v-divider></v-divider>
            <slot name="menu"></slot>
            <v-spacer></v-spacer>
            <v-divider></v-divider>
            <v-list-item link title="Logout" @click="logout"></v-list-item>
        </v-navigation-drawer>
        <v-main>
            <slot name="content"></slot>
        </v-main>
    </v-layout>
</template>

<script setup>
import { useUserStore } from "@/stores/UserStore";
import { ref, computed } from 'vue';
import { useRoute, useRouter } from "vue-router";
import { BASE_URL } from "@/stores/contants.js";


const userStore = useUserStore();
const token = userStore.getToken;
const route = useRoute();
const router = useRouter();

const logout = () => {
    userStore.logOut().then(() => {
        router.push('/login');
    });
}

</script>


<style lang="scss">

</style>