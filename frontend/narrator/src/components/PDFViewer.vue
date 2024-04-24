<template>
    <div class="pdf-ctn">
        <p>PDF viewer </p>
        <VuePDF :pdf="pdf"/>
    </div>
</template>


<script setup>

import { VuePDF, usePDF } from '@tato30/vue-pdf'
import '@tato30/vue-pdf/style.css'

const { pdf } = usePDF("../assets/NLP-D-24-00048.pdf")
// const { pdf } = usePDF("https://raw.githubusercontent.com/mozilla/pdf.js/ba2edeae/web/compressed.tracemonkey-pldi-09.pdf")
// console.log(`Document has ${pages} pages`)
// console.log(`Document info: ${info}`)
console.log(pdf)

</script>


<style lang="scss">
.pdf-ctn{
    width: 100%;
    height: 100%;
    min-height: 90vh;
    min-width: 400px;
    background-color: grey;
}
</style>