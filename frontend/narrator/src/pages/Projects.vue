<template>
    <v-navigation-drawer>
        <v-list-item title="Narrator" subtitle="automatic data abstraction tool"></v-list-item>
        <v-divider></v-divider>
        <v-list-item link active title="projects" to="/"></v-list-item>
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
                    width="1024">
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
                                        sm="6"
                                        md="4">
                                        <v-text-field
                                            label="Project name*"
                                            required
                                            v-model="pname"
                                        ></v-text-field>
                                    </v-col>
                                    <v-col
                                        cols="12"
                                        sm="6"
                                        md="4">
                                        <v-file-input
                                        multiple
                                        label="Documents"
                                        hint="upload the pdf documents you want to extract information from"
                                        ></v-file-input>
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
                    v-for="(item, index) in projectStore.getProjectsList"
                    :key="item.id"
                    :index="index"
                    cols="12"
                    sm="3">
                    <v-sheet class="ma-2 pa-2">
                        <ProjectItem 
                            :name="item.name"
                            :create_date="item.create_date">
                        </ProjectItem>
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

export default {
    setup() {
        const userStore = useUserStore();
        const projectStore = useProjectStore();
        projectStore.getProjects(userStore.getToken);
        return { 
            userStore,
            projectStore
        };
    },

    data(){
        return {
            dialog: false,
            pname: null,
        }
    },

    methods:{
        async logout(){
            await this.userStore.logOut().then(() => {
                this.$router.push(this.$route.query.redirect || '/login');
            });
        },
        async addProject(){
            this.projectStore.addProject(this.pname, this.userStore.getToken);
            this.projectStore.getProjects(this.userStore.getToken);
            this.dialog = false;
        }
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
}
</style>