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
            <v-btn density="compact" icon="mdi-upload" title="upload your documents here"></v-btn>
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
                            <DataTable :data="data" class="display" :options="options">
                                <thead>
                                    <tr>
                                        <th>First</th>
                                        <th>Second</th>
                                    </tr>
                                </thead>
                            </DataTable>
                        </v-window-item>
                        <v-window-item value="2">
                            <DataTable :data="data" class="display" :options="options">
                                <thead>
                                    <tr>
                                        <th>First</th>
                                        <th>Second</th>
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

DataTable.use(DataTablesCore);

const userStore = useUserStore();
const projectStore = useProjectStore();
const token = userStore.getToken;
const data = [
    [1, 2],
    [3, 4],
];
const options = {
    responsive: true,
    select: true,
};
const tab = ref('');
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