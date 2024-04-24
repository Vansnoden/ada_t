<template>
    <AuthLayout>
        <template v-slot:content>
            <v-container class="registration-ctn">
                <v-row class="mctn">
                    <v-col cols="12" sm="7" xs="12" md="4">
                        <v-form @submit.prevent="signup">
                            <v-card class="mcard">
                                <v-card-title>
                                    <h5 class="title">Welcome to ADA_T (PDF)</h5>
                                </v-card-title>
                                <v-card-text>
                                    <h5 class="mtitle">Join us, create an account here.</h5>
                                    <v-text-field type="text" label="username" v-model="username"></v-text-field>
                                    <v-text-field type="text" label="full name" v-model="fullname"></v-text-field>
                                    <v-text-field type="email" label="email" v-model="email"></v-text-field>
                                    <v-text-field type="password" label="password" v-model="password"></v-text-field>
                                    <v-text-field type="password" label="confirm password" v-model="cpassword"></v-text-field>
                                    
                                    <div class="errors" v-if="errors">
                                        😢 
                                        <span>{{ errors }}</span>
                                    </div>
                                </v-card-text>
                                <v-card-actions class="actions">
                                    <v-btn color="primary" variant="text" type="submit">Submit</v-btn>
                                    <div class="info-box">
                                        <span>Already have an account?</span>
                                        <router-link to="/login">log in here.</router-link>
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
import { useUserStore } from "@/stores/UserStore";
import AuthLayout from "./partials/AuthLayout.vue";

export default {
    setup() {
        const userStore = useUserStore();
        return { userStore };
    },
    data() {
        return {
            username: "",
            fullname: "",
            email: "",
            password: "",
            cpassword: "",
            errors: null
        };
    },

    // TODO: solve the double-click before redirection problem

    methods: {
        async signup() {
            if(this.password == this.cpassword){
                await this.userStore.signUp(this.username, this.fullname, this.email, this.password)
                .then(()=>{
                    if (this.userStore.getUser){
                        this.$router.push(this.$route.query.redirect || '/login');
                    }else{
                        console.log("We re in the else")
                        this.errors = this.userStore.getError
                    }
                }).catch(error => { 
                    this.errors += "\n"+error;
                })
            }else{
                this.errors += "\n"+"Passwords are not the same";
            }
        }
    },
}
</script>


<style lang="scss">
.registration-ctn{
    height:100%;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    color: #000;
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
    .errors{
        margin-top: 2em;
        color: red;
    }
    .actions{
        display: flex;
        flex-direction: column;
        gap:1em;
    }
}
</style>