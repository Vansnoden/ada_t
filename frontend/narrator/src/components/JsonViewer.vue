<template>
    <JsonEditorVue v-model="value"/>
</template>

<script setup>
import JsonEditorVue from 'json-editor-vue'
const value={
    "name":"paul",
    "email": "Thomas"
}
</script>

<style lang="scss">
</style>