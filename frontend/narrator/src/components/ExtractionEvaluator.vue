<template>
    <div class="ee-ctn">
        <v-card>
            <v-card-title>
                <div class="header">
                    <span>Evaluation</span>
                    <v-btn prepend-icon="mdi-content-save-outline" text="save" color="primary" @click="saveEvaluation"/>
                </div>
            </v-card-title>
            <v-card-text>
                <table class="mtable">
                    <tr v-for="question in questions" :key="question.id" :index="question.id">
                        <td>
                            {{ question.label }}
                        </td>
                        <td class="put-line">
                            <v-btn v-bind:variant="eval_value[question.id.toString()] ? 'elevated' : 'outlined'" 
                            icon="mdi-check" @click="validateAns(this, question.id)" color="green"></v-btn>
                        </td>
                        <td>
                            <v-btn v-bind:variant="!eval_value[question.id.toString()] ? 'elevated' : 'outlined'"
                            icon="mdi-close" @click="invalidateAns(question.id)" color="red"></v-btn>
                        </td>
                    </tr>
                </table>
            </v-card-text>
        </v-card>
    </div>
</template>

<script setup>
import { ref } from 'vue';
const props = defineProps(['path', 'questions']);
// questions is a json list
// path is just a string
const eval_value = ref({})
const button_models = ref({})

const validateAns = (el, qid) => {
    eval_value.value[""+qid] = true;
    console.log(eval_value.value);
}

const invalidateAns = (qid) => {
    eval_value.value[""+qid] = false;
    console.log(eval_value.value);
}

const saveEvaluation = () => {
    if(confirm("Are you sure?")){
        console.log("doing stuff ...");
        console.log(props.path);
    }
}


</script>


<style lang="scss">
.ee-ctn{
    box-sizing: border-box;
    padding-top: 1em;
    .header{
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid grey;
        padding-bottom: 0.5em;
    }
    .mtable{
        td{
            padding-left: 1em;
            padding-right: 1em;
        }
        .put-line{
            border-left: 1px solid grey;
        }
    }
}
</style>