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
                        <v-btn size="small" v-bind="props" prepend-icon="mdi-upload">
                            upload documents
                        </v-btn>
                    </template>
                    <v-card>
                        <v-card-title>
                            <span class="text-h5">Upload files</span>
                        </v-card-title>
                        <v-card-text>
                            <v-container>
                                <v-form @submit.prevent="uploadFiles" enctype="multipart/form-data">
                                    <v-row>
                                        <v-col cols="12" sm="12" md="12">
                                            <v-file-input required="true" name="files" @change="getFileInputValue" show-size
                                                counter multiple label="Upload all the files of these project"
                                                :rules="rules" accept="application/pdf">
                                            </v-file-input>
                                        </v-col>
                                    </v-row>
                                    <v-row>
                                        <v-col>
                                            <v-btn color="danger" variant="text" type="cancel"
                                                @click="closeFU">cancel</v-btn>
                                            <v-btn color="success" variant="text" type="submit">Submit</v-btn>
                                        </v-col>
                                    </v-row>
                                </v-form>
                            </v-container>
                        </v-card-text>
                    </v-card>
                </v-dialog>
            </div>
            <v-btn size="small" prepend-icon="mdi-play" class="success">
                run extraction
            </v-btn>
            <v-btn size="small" prepend-icon="mdi-stop" class="danger">
                stop extraction
            </v-btn>
            <v-btn size="small" prepend-icon="mdi-download">
                get results
            </v-btn>
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
                            <v-data-table :headers="doc_headers" :items="docs" :sort-by="[{ key: 'name', order: 'asc' }]">
                                <template v-slot:item.actions="{ item }">
                                    <v-btn size="small" color="red" prepend-icon="mdi-delete" v-bind="activatorProps"
                                        @click="deleteDoc(item.server_path)">
                                        Delete
                                    </v-btn>
                                </template>
                                <template v-slot:no-data>
                                    <v-btn color="primary" @click="initializeDocs">
                                        Refresh
                                    </v-btn>
                                </template>
                            </v-data-table>
                        </v-window-item>
                        <v-window-item value="2">
                            <v-data-table :headers="qa_headers" :items="qa">
                                <template v-slot:top>
                                    <v-toolbar flat>
                                        <v-toolbar-title></v-toolbar-title>
                                        <v-spacer></v-spacer>
                                        <v-dialog v-model="cqa_dialog" max-width="500px">
                                            <template v-slot:activator="{ props: activatorProps }">
                                                <v-btn size="small" class="default mr-1" color="primary"
                                                    prepend-icon="mdi-plus" v-bind="activatorProps">
                                                    New question
                                                </v-btn>
                                            </template>
                                            <v-card prepend-icon="mdi-pencil" title="New question">
                                                <v-card-text>
                                                    <v-form @submit.prevent="closeCreateQA">
                                                        <v-row dense>
                                                            <v-text-field name="label" label="Question label"
                                                                v-model="formAddQA.label"></v-text-field>
                                                        </v-row>
                                                        <v-row dense>
                                                            <span>Define answer format below with keys and data types for
                                                                each
                                                                keys.</span>
                                                            <v-btn prepend-icon="mdi-plus" class="mr-1"
                                                                @click="increment_keynum">add row</v-btn>
                                                            <v-btn prepend-icon="mdi-minus" @click="decrement_keynum">remove
                                                                last
                                                                row</v-btn>
                                                        </v-row>

                                                        <v-row class="stretch-row" v-for="i in keyNum">
                                                            <v-col cols="12" sm="6" md="6" xs="12">
                                                                <v-text-field label="Key"
                                                                    v-model="formAddQA['key' + i]"></v-text-field>
                                                            </v-col>
                                                            <v-col cols="12" sm="6" md="6" xs="12">
                                                                <v-select label="Select" v-model="formAddQA['type' + i]"
                                                                    :items="qa_types"></v-select>
                                                            </v-col>
                                                        </v-row>
                                                        <v-spacer></v-spacer>
                                                        <v-btn color="blue-darken-1" type="reset" variant="text"
                                                            @click="closeCreateQA">Cancel</v-btn>
                                                        <v-btn color="blue-darken-1" variant="text" type="submit">OK</v-btn>
                                                    </v-form>
                                                </v-card-text>
                                            </v-card>
                                        </v-dialog>
                                    </v-toolbar>
                                </template>
                                <template v-slot:item.actions="{ item }">
                                    <v-btn size="small" color="red" prepend-icon="mdi-delete"
                                        @click="deleteQA(item.id)">
                                        Delete
                                    </v-btn>
                                </template>
                                <template v-slot:no-data>
                                    <v-btn color="primary" @click="initializeQA">
                                        Refresh
                                    </v-btn>
                                </template>
                            </v-data-table>
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
import { ref, computed } from 'vue';
import { useRoute, useRouter } from "vue-router";
import { BASE_URL } from "@/stores/contants.js";

DataTable.use(DataTablesCore);


const userStore = useUserStore();
const projectStore = useProjectStore();
const token = userStore.getToken;
const route = useRoute();
const router = useRouter();
const project = projectStore.getSingleProject(route.params.id);
const docs = ref("docs");
docs.value = [];
const qa = ref("qa");
qa.value = [];
const formUpload = ref('formUpload');

const getProjectDocuments = (id, token) => {
    var myHeaders = new Headers();
    myHeaders.append("Authorization", token);
    var requestOptions = {
        method: 'POST',
        headers: myHeaders
    };
    fetch(BASE_URL + "/project/" + id + "/files", requestOptions)
        .then(res => res.json())
        .then((response) => {
            docs.value = response;
        });
}

const getProjectQuestions = (id, token) => {
    var myHeaders = new Headers();
    myHeaders.append("Authorization", token);
    var requestOptions = {
        method: 'GET',
        headers: myHeaders
    };
    fetch(BASE_URL + "/questions/" + id, requestOptions)
        .then(res => res.json())
        .then((response) => {
            qa.value = response;
        });
}
getProjectDocuments(route.params.id, token);
getProjectQuestions(route.params.id, token);


// using vuetify datatables

// project documents
const doc_headers = [
    { title: 'Name', key: 'name', sortable: true, align: 'start' },
    { title: 'Actions', key: 'actions', sortable: false },
]

// question data
const qa_headers = [
    { title: 'Label', key: 'label', sortable: true, align: 'start' },
    { title: 'Actions', key: 'actions', sortable: false },
]

const qa_types = ['string', 'array'];

const keyNum = ref('keyNum');
keyNum.value = 1;

const increment_keynum = () => {
    keyNum.value = keyNum.value + 1;
}

const decrement_keynum = () => {
    keyNum.value = keyNum.value - 1;
    if (keyNum.value < 0) {
        keyNum.value = 0;
    }
}

const tab = ref('tab');
const fu_dialog = ref('fu_dialog');
fu_dialog.value = false;
const da_dialog = ref('da_dialog');
da_dialog.value = false;
const dqa_dialog = ref('dqa_dialog');
dqa_dialog.value = false;
const eqa_dialog = ref('eqa_dialog');
eqa_dialog.value = false;
const cqa_dialog = ref('cqa_dialog');
cqa_dialog.value = false;
const dd_dialog = ref('dd_dialog');
dd_dialog.value = false;
const editedItem = ref('editedItem');
const files = ref(); //files to be uploaded
const formAddQA = ref();
formAddQA.value = {} //object to keep form values when creating question

const closeFU = () => {
    fu_dialog.value = false;
}

const rules = [
    value => {
        if (value) return true
        return 'You must provide at least one file'
    },
]


const deleteDoc = (serverPath) => {
    if (window.confirm('Do you confirm?')) {
        const myHeaders = new Headers();
        myHeaders.append("Authorization", token);
        myHeaders.append("Content-Type", "application/json");

        const raw = JSON.stringify({
            "file_path": serverPath
        });

        const requestOptions = {
          method: "POST",
          headers: myHeaders,
          body: raw,
          redirect: "follow"
        };

        fetch(BASE_URL + "/delete_file", requestOptions)
          .then((response) => response.text())
          .then((result) => initializeDocs())
          .catch((error) => console.error(error));
    } else {

    }
}

const deleteDocConfirm = () => {
    console.log("document deletion confirmed ...");
    dd_dialog.value = false;
}

// questions
const deleteQA = (id) => {
    if (window.confirm('Are you sure you want to delete this question?')) {
        const myHeaders = new Headers();
        myHeaders.append("Authorization", token);

        const requestOptions = {
          method: "GET",
          headers: myHeaders,
          redirect: "follow"
        };

        fetch(BASE_URL + "/questions/delete/"+id, requestOptions)
          .then((response) => response.text())
          .then((result) => initializeQA())
          .catch((error) => console.error(error));
    } else {

    }
}


const closeEditQA = () => {
    eqa_dialog.value = false;
}


const closeCreateQA = () => {
    let label = formAddQA.value.label;
    delete formAddQA.value['label'];
    const myHeaders = new Headers();
    let answer_format = {};
    myHeaders.append("Authorization", token);
    myHeaders.append("Content-Type", "application/json");
    for (let i = 1; i <= keyNum.value; i++) {
        answer_format[formAddQA.value['key' + i]] = formAddQA.value['type' + i];
    }
    answer_format = JSON.stringify(answer_format);
    // JSON.stringify(answer_format).replace(/\\/g,"");
    
    var raw = JSON.stringify({
        "label": label,
        "answer_format": `${answer_format}`,
        "project_id": parseInt(route.params.id)
    });
    // .replace(/\\/g,"");

    console.log(raw);

    const requestOptions = {
        method: "POST",
        headers: myHeaders,
        body: raw,
        redirect: "follow"
    };
    fetch(BASE_URL + "/questions/", requestOptions)
        .then((response) => response.json())
        .then((result) => {
            initializeQA();
            cqa_dialog.value = false;
        })
        .catch((error) => console.error(error));
    cqa_dialog.value = false;
}

const editQA = (item) => {
    eqa_dialog.value = false;
}


const createQA = (item) => {
    cqa_dialog.value = false;
}


const logout = () => {
    userStore.logOut().then(() => {
        router.push('/login');
    });
}

const initializeDocs = () => {
    getProjectDocuments(route.params.id, token);
}

const initializeQA = () => {
    getProjectQuestions(route.params.id, token);
}

const getFileInputValue = (event) => {
    //get the file input value
    const mfiles = event.target.files;
    console.log("M-files");
    console.log(mfiles);
    //assign it to our reactive reference value 
    files.value = mfiles;
}

const uploadFiles = (id) => {
    fu_dialog.value = false;
    const myHeaders = new Headers();
    myHeaders.append("Authorization", token);

    const formdata = new FormData();

    console.log("FILESSSS");
    console.log(files.value);

    for (let i = 0; i < files.value.length; i++) {
        console.log("FILE X");
        console.log(files.value[i]);
        formdata.append("files", files.value[i], files.value[i].name);
    }
    console.log(formdata);

    const requestOptions = {
        method: "POST",
        headers: myHeaders,
        body: formdata,
        redirect: "follow"
    };

    fetch(BASE_URL + "/project/" + route.params.id + "/upload", requestOptions)
        .then((response) => response.text())
        .then((result) => {
            console.log(result);
            initializeDocs();
        })
        .catch((error) => console.error(error));
}
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

    .mr-1 {
        margin-right: 1em !important;
    }

    .content {
        padding: 1em;
    }

    .hint {
        color: grey;
        font-size: 0.8rem;
    }

    .mt-2 {
        margin-top: 4em !important;
    }

    .title {
        font-weight: 600;
    }

    .date {
        font-weight: lighter;
    }

    .danger {
        background-color: rgb(252, 155, 155);
        /* color: #fff; */
    }

    .success {
        background-color: rgb(108, 224, 108);
        /* color: #fff; */
    }

    .stretch-row {
        margin: 0 !important;
        padding: 0 !important;
    }
}
</style>