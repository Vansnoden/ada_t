<template>
    <AuthLayout>
        <template v-slot:content>
            <v-container class="login-ctn">
                <v-row class="mctn">
                    <v-col cols="12" sm="6" xs="12" md="3">
                        <v-form @submit.prevent="login">
                            <v-card class="mcard">
                                <v-card-title>
                                    <h5 class="title">Welcome to ADA_T (PDF)</h5>
                                </v-card-title>
                                <v-card-text>
                                    <h5 class="mtitle">Login is required</h5>
                                    <v-text-field type="text" label="username" v-model="username"></v-text-field>
                                    <v-text-field type="password" label="password" v-model="password"></v-text-field>
                                    <div class="errors" v-if="errors">
                                        😢 
                                        <span>{{ errors }}</span>
                                    </div>
                                </v-card-text>
                                <v-card-actions class="actions">
                                    <v-btn color="primary" variant="text" type="submit">Submit</v-btn>
                                    <div class="info-box">
                                        <span>Do not have an account yet ?</span>
                                        <router-link to="/register">Create one here.</router-link>
                                    </div>
                                </v-card-actions>
                            </v-card>
                        </v-form>
                    </v-col>
                </v-row>
            </v-container>
        </template>
    </AuthLayout>
</template>

<script>
// 
import { useUserStore } from "@/stores/UserStore";
import { storeToRefs } from 'pinia';
import AuthLayout from "./partials/AuthLayout.vue";

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
.login-ctn{
    // background-color: skyblue;
    height:100%;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    color: #000;

    .mcard{
        padding: 1em!important;
        width: 100%;
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
        span{
            margin-right: 1em;
        }
    }

    .actions{
        display: flex;
        flex-direction: column;
        gap:1em;
    }

    .errors{
        margin-top: 2em;
        color: red;
    }
}
</style>