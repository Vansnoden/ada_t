<template>
    <DashboardLayout>
        <template v-slot:menu>
            <v-list-item link active title="Projects" to="/projects"></v-list-item>
            <v-list-item link title="Account settings"></v-list-item>
            <v-list-item link title="Userguide"></v-list-item>
            <v-list-item link title="Help?"></v-list-item>
        </template>
        <template v-slot:content>
            <v-container fluid class="doc-ctn">
                <v-row>
                    <v-col cols="12" md="6" xs="12">
                        <PDFViewer></PDFViewer>
                    </v-col>
                    <v-col cols="12" md="6" xs="12">
                        <JsonViewer></JsonViewer>
                    </v-col>
                </v-row>
            </v-container>
            <Footer></Footer>
        </template>
    </DashboardLayout>
</template>


<script setup>
import DashboardLayout from '@/layouts/DashboardLayout.vue';
import JsonViewer from '@/components/JsonViewer.vue';
import { ref, computed } from 'vue';
import { useRoute, useRouter } from "vue-router";
import { BASE_URL } from "@/stores/contants.js";
import PDFViewer from '@/components/PDFViewer.vue'


const route = useRoute();
const router = useRouter();
const file_path = route.query.server_path
</script>

<style lang="scss">
.doc-ctn{
    height: 93vh;
    box-sizing: border-box;
    padding: 1em;
    overflow-y: scroll!important;
}
</style>