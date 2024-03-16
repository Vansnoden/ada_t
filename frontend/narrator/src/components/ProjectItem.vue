<template>
    <div class="project-item">
        <v-card 
            :title="name" 
            :text="'created on: '+create_date" prepend-icon="mdi-content-paste">
            <v-card-actions>
                <v-btn class="btn-danger" elevation="2" @click="on_delete">
                    <v-icon>mdi-delete-forever</v-icon>
                    Delete
                </v-btn>
                <v-btn class="btn-success" elevation="2" @click="on_edit">
                    <v-icon>mdi-open-in-new</v-icon>
                    Open
                </v-btn>
            </v-card-actions>
        </v-card>
    </div>
</template>


<script>
import { useUserStore } from "@/stores/UserStore";
import { useProjectStore } from "@/stores/ProjectStore";
import { storeToRefs } from 'pinia';
import { computed } from 'vue';

export default {
    props: ['id', 'name', 'create_date'],
    setup(props) {
        const userStore = useUserStore();
        const projectStore = useProjectStore();
        const token = userStore.getToken;
        projectStore.getProjects(token);
        return {
            props,
            useUserStore,
            projectStore,
            token
        }
    },

    data(){

    },

    methods:{
        async details(){
            console.log('open details page...');
        },

        deleteProject(){
            this.projectStore.removeProject(id, this.token);
        },

        editProject(){
            console.log('attempting project edition'+ id);
        }

    }
};
</script>


<style lang="scss">
.project-item{
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