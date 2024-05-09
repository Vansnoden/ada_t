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
                            <div class="results">
                                <v-card class="mb-3">
                                    <v-card-title>Model outputs</v-card-title>
                                    <v-card-text>
                                        <JsonViewer v-model="model_answers.data" :data="model_answers.data"></JsonViewer>
                                    </v-card-text>
                                </v-card>
                            </div>
                            <div class="eval">
                                <ExtractionEvaluator :path="file_path" :questions="questions"></ExtractionEvaluator>
                            </div>
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
import ExtractionEvaluator from '@/components/ExtractionEvaluator.vue'

const route = useRoute();
const router = useRouter();
const file_path = route.query.server_path;
const url = BASE_URL + "/download?file_path="+file_path;
const model_answers = ref({});

const questions = [
  {
    "label": "what is the title of this study ?",
    "answer_format": "{\"title\": \"string\"}",
    "project_id": 1,
    "id": 1,
    "is_active": true,
    "create_date": "2024-04-30T05:00:20.360979",
    "anwser_grammar": "/code/database/resources/1/grammars/1.gbnf"
  },
  {
    "label": "who are the authors of this study ?",
    "answer_format": "[{\"name\": \"string\"}]",
    "project_id": 1,
    "id": 2,
    "is_active": true,
    "create_date": "2024-04-30T05:00:20.360979",
    "anwser_grammar": "/code/database/resources/1/grammars/2.gbnf"
  },
  {
    "label": "in what year was the study published ?",
    "answer_format": "{\"publish_year\": \"string\"}",
    "project_id": 1,
    "id": 3,
    "is_active": true,
    "create_date": "2024-04-30T05:00:20.360979",
    "anwser_grammar": "/code/database/resources/1/grammars/3.gbnf"
  },
  {
    "label": "what vector species are studied in this study ?",
    "answer_format": "[{\"specie_name\": \"string\"}]",
    "project_id": 1,
    "id": 4,
    "is_active": true,
    "create_date": "2024-04-30T05:00:20.360979",
    "anwser_grammar": "/code/database/resources/1/grammars/4.gbnf"
  },
  {
    "label": "in what country and site or location was the study carried out?",
    "answer_format": "[{\"country_name\": \"string\", \"location_name\": \"string\"}]",
    "project_id": 1,
    "id": 5,
    "is_active": true,
    "create_date": "2024-04-30T05:00:20.360979",
    "anwser_grammar": "/code/database/resources/1/grammars/5.gbnf"
  }
]

const refreshResults = () => {
    fetch(BASE_URL + "/download?file_path="+ route.query.results_path)
    .then(response => response.json())
    .then((results)=>{
        model_answers.value.data = results;
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
    .results{
        height: 45vh;
        overflow: scroll;
        border: 1px solid grey;
        border-radius: 10px;
        padding: 0.5em;
        margin-bottom: 0.5em;
    }
    .eval{
        height: 45vh;
        overflow: scroll;
        border: 1px solid grey;
        border-radius: 10px;
        padding: 0.5em;
    }
}
</style>