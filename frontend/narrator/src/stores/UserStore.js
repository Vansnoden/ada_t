import { defineStore } from 'pinia'
// import user from "@/data/user.json"

// You can name the return value of `defineStore()` anything you want,
// but it's best to use the name of the store and surround it with `use`
// and `Store` (e.g. `useUserStore`, `useCartStore`, `useProductStore`)
// the first argument is a unique id of the store across your application
import {BASE_URL} from "@/stores/contants.js"

export const useUserStore = defineStore({
    // id
    id: 'UserStore',
    // state
    state: ()=>({ 
        user: null,
        token: null,
        token_type: null,
        error: null
    }),
    // persist store state
    persist: true,
    // actions
    actions:{
        async signUp(username, fullname, email, password) {
            fetch(BASE_URL + "/users", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ 
                    "username":username, 
                    "fullname":fullname,
                    "email": email, 
                    "password": password 
                }),
            }).then(response => response.json())
            .then(res => {
                if (res.username){
                    this.user = res;
                }else{
                    this.error = res.detail
                }
            }).catch(error=>console.log('error getting user details', error))
        },

        async signIn(username, password) {
            var formdata = new FormData();
            formdata.append("username", username);
            formdata.append("password", password);
            fetch(BASE_URL + "/token", {
                method: 'POST',
                body: formdata,
            }).then(response => response.json())
            .then(results => {
                this.token = results.access_token;
                this.token_type = results.token_type
            }).then(() => {
                // get auth user details
                var myHeaders = new Headers();
                myHeaders.append("Authorization", this.token_type + " " + this.token); 
                fetch(BASE_URL + "/users/details/me", {
                    method: "GET",
                    headers: myHeaders
                }).then(response => response.json())
                .then(results => {
                    if (results.username){
                        this.user = results;
                    }else{
                        this.error = res.detail
                    }
                }).catch(error => console.log('error getting user details', error));
            })
            .catch(error => console.log('authentication error', error));
        },

        async logOut(){
            this.user = null
            this.token = null
            this.token_type = null
        }
    },
    // getters
    getters: {
        getUser: (state) => state.user,
        getToken: (state) => state.token_type + " " + state.token,
        getError:  (state) => state.error
    }
})