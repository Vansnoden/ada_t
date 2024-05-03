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
                    <v-col cols="12" md="7" xs="12">
                        <PDFViewer :url="url"
                        ></PDFViewer>
                    </v-col>
                    <v-col cols="12" md="5" xs="12">
                        <div class="sticky">
                            <JsonViewer v-model="model_answers.data" :data="model_answers.data"></JsonViewer>
                        </div>
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
import { ref, reactive, computed, onMounted } from 'vue';
import { useRoute, useRouter } from "vue-router";
import { BASE_URL } from "@/stores/contants.js";
import PDFViewer from '@/components/PDFViewer.vue';


const route = useRoute();
const router = useRouter();
const file_path = route.query.server_path;
const url = BASE_URL + "/download?file_path="+file_path;
const model_answers = ref({});

const refreshResults = () => {
    fetch(BASE_URL + "/download?file_path="+ route.query.results_path)
    .then(response => response.json())
    .then((results)=>{
        model_answers.value.data = results;
        console.log(results)
        console.log(model_answers.value.data);
    });
}

onMounted(()=>{
    refreshResults();
})

</script>

<style lang="scss">
.doc-ctn{
    height: 93vh;
    box-sizing: border-box;
    padding: 1em;
    overflow-y: scroll!important;

    .sticky{
        position: -webkit-sticky; /* Safari */
        position: sticky;
        top: 0;
    }
}
</style>