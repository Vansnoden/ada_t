<template>
    <v-navigation-drawer>
        <v-list-item title="Narrator" subtitle="automatic data abstraction tool"></v-list-item>
        <v-divider></v-divider>
        <v-list-item link active title="projects" to="/projects"></v-list-item>
        <v-list-item link title="account settings"></v-list-item>
        <v-list-item link title="userguide"></v-list-item>
        <v-list-item link title="help?"></v-list-item>
        <v-spacer></v-spacer>
        <v-divider></v-divider>
        <v-list-item link title="logout" @click="logout"></v-list-item>
    </v-navigation-drawer>
    <div class="project_page">
        <div class="toolbar">
            <div>
                <v-dialog v-model="fu_dialog" persistent width="512">
                    <template v-slot:activator="{ props }">
                        <v-btn density="compact" v-bind="props" icon="mdi-upload"
                            title="upload your documents here"></v-btn>
                    </template>
                    <v-card>
                        <v-card-title>
                            <span class="text-h5">Upload files</span>
                        </v-card-title>
                        <v-card-text>
                            <v-container>
                                <v-form @submit.prevent="uploadFiles">
                                    <v-row>
                                        <v-col cols="12" sm="12" md="12">
                                            <v-file-input required="true" name="files" show-size counter multiple
                                                label="Upload all the files of these project" :rules="rules"
                                                accept="application/pdf">
                                            </v-file-input>
                                        </v-col>
                                    </v-row>
                                    <v-row>
                                        <v-col>
                                            <v-btn color="primary" variant="text" type="submit">Submit</v-btn>
                                        </v-col>
                                    </v-row>
                                </v-form>
                            </v-container>
                        </v-card-text>
                    </v-card>
                </v-dialog>
            </div>
            <v-btn density="compact" icon="mdi-play" class="success" title="run extraction here"></v-btn>
            <v-btn density="compact" icon="mdi-stop" class="danger" title="stop all extractions here"></v-btn>
            <v-btn density="compact" icon="mdi-download" title="download extraction results here"></v-btn>
        </div>
        <div class="content">
            <v-card>
                <v-tabs v-model="tab" bg-color="secondary" align-tabs="center">
                    <v-tab value="1">Documents</v-tab>
                    <v-tab value="2">Questionnaire</v-tab>
                </v-tabs>
                <v-card-text>
                    <v-window v-model="tab">
                        <v-window-item value="1">
                            <DataTable class="display" :options="options" :columns="dataDocCols" :data="dataDoc">
                                <thead>
                                    <tr>
                                        <th>Name</th>
                                        <th>Status</th>
                                    </tr>
                                </thead>
                            </DataTable>
                        </v-window-item>
                        <v-window-item value="2">
                            <DataTable :columns="dataQaCols" :data="dataQa" class="display" :options="options">
                                <thead>
                                    <tr>
                                        <th>Label</th>
                                    </tr>
                                </thead>
                            </DataTable>
                        </v-window-item>
                    </v-window>
                </v-card-text>
            </v-card>
        </div>
    </div>
</template>

<script setup>
import { useUserStore } from "@/stores/UserStore";
import { useProjectStore } from "@/stores/ProjectStore";
// import { storeToRefs } from 'pinia';
// import { computed } from 'vue';
// others
import DataTable from 'datatables.net-vue3';
import DataTablesCore from 'datatables.net';
import 'datatables.net-select';
import 'datatables.net-responsive';
import { ref } from 'vue';
import { useRoute } from "vue-router";

DataTable.use(DataTablesCore);


const userStore = useUserStore();
const projectStore = useProjectStore();
const token = userStore.getToken;
const route = useRoute();
const project = projectStore.getSingleProject(route.params.id);
const projectDocs = projectStore.getProjectDocuments(route.params.id, token);

// document data
const dataDocCols = [
    { data: 'name' },
    { data: 'status' },
]
const dataDoc = [
    {
        'name': 'first document',
        'status': "draft",
    },
    {
        'name': 'second document',
        'status': "draft",
    }
];

// question data
const dataQaCols = [
    { data: 'label' },
]
const dataQa = [
    {
        'label': 'what is the title of this study?',
    },
    {
        'label': 'who are th autors of this study?',
    }
];


const options = {
    responsive: true,
    select: false,
};
const tab = ref('tab');
const fu_dialog = ref('fu_dialog');
const files = ref('files'); //files to be uploaded
fu_dialog.value = false;

const download = (id) => {
    console.log('download')
}

const uploadFiles = (id) => {
    console.log(files);
    fu_dialog.value = false;
}

const rules = [
    value => {
        if (value) return true
        return 'You must provide at least one file'
    },
]

</script>


<style lang="scss">
@import 'datatables.net-dt';

.project_page {
    color: #000;
    min-height: 93vh !important;

    .toolbar {
        border-bottom: 1px solid lightgrey;
        padding: 1em;
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
        gap: 2em;
    }

    .content {
        padding: 1em;
    }

    .hint {
        color: grey;
        font-size: 0.8rem;
    }

    .title {
        font-weight: 600;
    }

    .date {
        font-weight: lighter;
    }

    .danger {
        background-color: rgb(252, 155, 155);
        // color: #fff;
    }

    .success {
        background-color: rgb(108, 224, 108);
        // color: #fff;
    }
}
</style>