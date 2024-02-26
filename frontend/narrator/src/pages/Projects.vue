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
    <div class="projects">
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
        <div class="content">
            <div style="margin-bottom:2em">
                Welcome back dear <b><i>{{ userStore.user.username }}</i></b> !<br/>
            </div>
            <p class="hint" v-if="!projectStore.getProjectsList">You haven't initiated any project yet ...</p>
            <v-container fluid>
                <v-row no-gutters>
                <v-col
                    v-for="item in projectStore.getProjectsList"
                    :key="item.id"
                    :index="item.id"
                    cols="12"
                    sm="3">
                    <v-sheet class="ma-2 pa-2">
                        <v-card 
                            :title="item.name" 
                            :text="'created on: '+item.create_date" prepend-icon="mdi-content-paste">
                            <v-card-actions>
                                <v-btn class="btn-danger" elevation="2">
                                    <v-icon>mdi-delete-forever</v-icon>
                                    Delete
                                </v-btn>
                                <v-btn class="btn-success" elevation="2">
                                    <v-icon>mdi-open-in-new</v-icon>
                                    Open
                                </v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-sheet>
                </v-col>
                </v-row>
            </v-container>
        </div>
    </div>
    <Footer></Footer>
</template>

<script>
// 
import { useUserStore } from "@/stores/UserStore";
import { useProjectStore } from "@/stores/ProjectStore";
import { storeToRefs } from 'pinia';
import { computed } from 'vue';

export default {
    setup() {
        const userStore = useUserStore();
        const projectStore = useProjectStore();
        const token = userStore.getToken;
        projectStore.getProjects(token);
        // const projects = computed(() => projectStore.getProjectsList);
        // const { getProjectsList } = storeToRefs(projectStore);
        return { 
            userStore,
            projectStore,
            token
        };
    },


    data(){
        return {
            dialog: false,
            pname: null,
        }
    },

    methods:{
        logout(){
            this.userStore.logOut().then(() => {
                this.$router.push(this.$route.query.redirect || '/login');
            });
        },
        addProject(){
            this.projectStore.addProject(this.pname, this.token);
            // this.projectStore.getProjects(this.token);
            this.dialog = false;
        },
    }

};
</script>


<style lang="scss">
.projects{
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