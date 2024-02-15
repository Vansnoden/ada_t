<template>
    <div class="registration">
        <v-container class="mctn">
            <v-row>
                <v-col cols="12" sm="10" md="6" lg="4">
                    <v-card class="mcard">
                        <v-sheet>
                            <v-form @submit.prevent="signup">
                                <h5 class="mtitle">Join us, create an account here.</h5>
                                <v-text-field type="text" label="username" v-model="username"></v-text-field>
                                <v-text-field type="text" label="full name" v-model="fullname"></v-text-field>
                                <v-text-field type="email" label="email" v-model="email"></v-text-field>
                                <v-text-field type="password" label="password" v-model="password"></v-text-field>
                                <v-text-field type="password" label="confirm password" v-model="cpassword"></v-text-field>
                                <v-btn color="primary" variant="text" type="submit">Submit</v-btn>
                                <div class="info-box">
                                    <span>Already have an account?</span>
                                    <router-link to="/login">log in here.</router-link>
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
import { useUserStore } from "@/stores/UserStore";
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
.registration{
    background-color: skyblue;
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
        background-color: skyblue;
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
    }
    .errors{
        margin-top: 2em;
        color: red;
    }
}
</style>