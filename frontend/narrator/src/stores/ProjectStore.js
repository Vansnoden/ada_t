import { defineStore } from 'pinia';
import {BASE_URL} from "@/stores/contants.js";
import {useUserStore} from "@/stores/UserStore.js"; 

export const useProjectStore = defineStore({
    id: "ProjectStore",

    state: ()=>({
        projects: []
    }),

    persist: true,

    actions: {
        async getProjects(token){
            var myHeaders = new Headers();
            myHeaders.append("Authorization", token);
            var requestOptions = {
                method: 'GET',
                headers: myHeaders
            };
            const res = await fetch(BASE_URL+"/projects", requestOptions);
            const data = await res.json();
            this.projects = data;
            return data;
        },

        async addProject(name, token){
            var myHeaders = new Headers();
            myHeaders.append("Content-Type", "application/json");
            myHeaders.append("Authorization", token);

            var raw = JSON.stringify({
                "name": name
            });

            var requestOptions = {
                method: 'POST',
                headers: myHeaders,
                body: raw
            };

            await fetch(BASE_URL+"/projects", requestOptions)
            .then((res) => {
                let response = res.json();
                for(let i=0; i<response.length; i++){
                    this.projects.push(response[i])
                }
            })
            .catch(error => {
                console.log('error', error);
                return false;
            });
            
            return true;
        },

        async removeProject(id, token){
            var myHeaders = new Headers();
            myHeaders.append("Content-Type", "application/json");
            myHeaders.append("Authorization", token);

            var requestOptions = {
                method: 'GET',
                headers: myHeaders,
            };

            await fetch(BASE_URL+"/projects/delete/"+id, requestOptions)
            .then((res) => {
                this.projects = this.getProjects(token);
                console.log(res.text());
            })
            .catch(error => {
                console.log('error', error);
                return false;
            });
            return true;
        }
    },

    getters: {
        getProjectsList: (state) => state.projects
    }
})
