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
            <v-row>
                <v-dialog
                    v-model="dialog"
                    persistent
                    width="512">
                    <template v-slot:activator="{ props }">
                        <v-btn
                            color="primary"
                            v-bind="props"
                            prepend-icon="mdi-plus"
                        >
                        New project
                        </v-btn>
                    </template>
                    <v-card>
                        <v-card-title>
                            <span class="text-h5">Project details</span>
                        </v-card-title>
                        <v-card-text>
                            <v-container>
                                <v-row>
                                    <v-col
                                        cols="12"
                                        sm="12"
                                        md="12">
                                        <v-text-field
                                            label="Project name*"
                                            required
                                            v-model="pname"
                                        ></v-text-field>
                                    </v-col>
                                </v-row>
                            </v-container>
                            <small>*indicates required field</small>
                        </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn
                            color="blue-darken-1"
                            variant="text"
                            @click="dialog = false">
                            Close
                        </v-btn>
                        <v-btn
                            color="blue-darken-1"
                            variant="text"
                            @click="addProject">
                            Save
                        </v-btn>
                    </v-card-actions>
                </v-card>
                </v-dialog>
            </v-row>
        </div>
    </div>
</template>
<script>
import { useUserStore } from "@/stores/UserStore";
import { useProjectStore } from "@/stores/ProjectStore";
import { storeToRefs } from 'pinia';
import { computed } from 'vue';

export default {
    setup() {
        const userStore = useUserStore();
        const projectStore = useProjectStore();
        const token = userStore.getToken;
        return { 
            userStore,
            projectStore,
            token
        };
    },
    data(){
        return{
            project
        }
    },
    async beforeRouteUpdate(to, from) {
        // react to route changes...
        this.project = this.projectStore.getSingleProject(this.token, to.params.id)
    },
    methods:{

    }
}
</script>
<style lang="scss">
.project_page{
    color: #000;
    min-height: 93vh!important;
    .toolbar{
        border-bottom: 1px solid lightgrey;
        padding: 1em;
        display: flex;
        flex-direction: row;
        justify-content: start;
        align-items: center;
        gap: 0.8em;
    }
    .content{
        padding: 1em;
    }
    .hint{
        color: grey;
        font-size: 0.8rem;
    }
    .title{
        font-weight: 600;
    }
    .date{
        font-weight: lighter;
    }
    .btn-danger{
        background-color:rgb(252, 155, 155);
        // color: #fff;
    }
    .btn-success{
        background-color: rgb(108, 224, 108);
        // color: #fff;
    }
}
</style>