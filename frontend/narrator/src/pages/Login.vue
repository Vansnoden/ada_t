<template>
    <div class="login">
        <!-- <video autoplay muted loop id="myVideo">
            <source src="../assets/deepdive.mp4" type="video/mp4">
        </video> -->
        <v-container class="mctn">
            <v-row>
                <v-col cols="12" sm="10" md="6" lg="4">
                    <h1 class="title">Welcome to ADA.T <small>(PDF)</small></h1>
                    <v-card class="mcard">
                        <v-sheet>
                            <v-form @submit.prevent="login">
                                <h5 class="mtitle">Login is required</h5>
                                <v-text-field type="text" label="username" v-model="username"></v-text-field>
                                <v-text-field type="password" label="password" v-model="password"></v-text-field>
                                <v-btn color="primary" variant="text" type="submit">Submit</v-btn>
                                <div class="info-box">
                                    <span>Do not have an account yet ?</span>
                                    <router-link to="/register">Create one here.</router-link>
                                </div>
                                <div class="errors" v-if="errors">
                                    😢 
                                    <span>{{ errors }}</span>
                                </div>
                            </v-form>
                        </v-sheet>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>

<script>
// 
import { useUserStore } from "@/stores/UserStore";
import { storeToRefs } from 'pinia';

export default {
    setup() {
        const userStore = useUserStore();
        const user = storeToRefs(userStore.getUser);
        return { userStore , user};
    },

    data() {
        return {
            username: "",
            password: "",
            errors: null,
            user: null
        };
    },

    methods: {
        async login() {
            await this.userStore.signIn(this.username, this.password)
            .then(()=>{
                if(this.user){
                    this.$router.push({ name:'projects'});
                }else{
                    this.errors="\n Wrong login or password";
                }
            }).catch(error => { 
                this.errors = error;
            })
        }
    },
};
</script>


<style lang="scss">
.login{
    background-color: skyblue;
    height:100%;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    color: #000;
    // .title{
    //     color:#fff;
    // }
    // #myVideo {
    //     position: fixed;
    //     right: 0;
    //     bottom: 0;
    //     min-width: 100%;
    //     min-height: 100%;
    //     z-index: 1;
    // }
    .mcard{
        padding: 1em!important;
    }

    .mtitle{
        font-weight: 1.5rem;
        margin-bottom: 1em;
    }
    .mctn{
        margin: auto!important;
        height:100%;
        display: flex!important;
        flex-direction: row!important;
        justify-content: center!important;
        align-items: center!important;
        z-index: 5;
    }
    .info-box{
        padding:1em;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-around;
        border: 1px solid lightgrey;
        border-radius: 5px;
        font-size: 0.8rem;
    }

    .errors{
        margin-top: 2em;
        color: red;
    }
}
</style>