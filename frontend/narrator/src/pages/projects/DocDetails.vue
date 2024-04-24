<template>
    <DashboardLayout>
        <template v-slot:menu>
            <v-list-item link active title="Projects" to="/projects"></v-list-item>
            <v-list-item link title="Account settings"></v-list-item>
            <v-list-item link title="Userguide"></v-list-item>
            <v-list-item link title="Help?"></v-list-item>
        </template>
        <template v-slot:content>
            <div class="doc-ctn">
                <p>Document details</p><br/>
                {{ file_path }}
            </div>
            <Footer></Footer>
        </template>
    </DashboardLayout>
</template>


<script setup>
import DashboardLayout from '@/layouts/DashboardLayout.vue';
import { ref, computed } from 'vue';
import { useRoute, useRouter } from "vue-router";
import { BASE_URL } from "@/stores/contants.js";

const route = useRoute();
const router = useRouter();
const file_path = route.query.server_path
</script>

<style lang="scss">
.doc-ctn{
    height: 93vh;
    box-sizing: border-box;
    padding: 1em;
}
</style>