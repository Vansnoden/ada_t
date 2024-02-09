<template>
    <div class="project-item">
        <v-card 
            :title="name" 
            :text="'created on: '+create_date" prepend-icon="mdi-content-paste">
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
    </div>
</template>


<script>
export default {
    props: ['name', 'create_date'],
    setup(props) {
        
    },

    data(){

    },

    methods:{
        async details(){
            console.log('open details page...');
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