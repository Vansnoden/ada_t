<template>
    <JsonEditorVue v-model="data"/>
</template>

<script setup>
import JsonEditorVue from 'json-editor-vue';
const props = defineProps(['data']);

const data= props.data;

</script>

<style lang="scss">
</style>