<template>
    <div class="login">
        <v-container class="mctn">
            <v-row>
                <v-col cols="12" sm="10" md="6" lg="4">
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
export default {
    setup() {
        const userStore = useUserStore();
        return { userStore };
    },
    data() {
        return {
            username: "",
            password: "",
            errors: null
        };
    },

    // TODO: solve the double-click before redirection problem

    methods: {
        async login() {
            await this.userStore.signIn(this.username, this.password)
            .then(()=>{
                if(this.userStore.getUser.username){
                    this.$router.push(this.$route.query.redirect || '/');
                }else{
                    this.errors="\n Wrong login or password";
                }
                // 
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