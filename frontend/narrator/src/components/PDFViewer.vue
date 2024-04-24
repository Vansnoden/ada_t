<template>
    <div class="pdf-ctn">
        <p>PDF viewer </p>
        <VuePdfEmbed annotation-layer text-layer
            image-resources-path="https://unpkg.com/pdfjs-dist/web/images/" 
            :source="{
                cMapUrl: 'https://unpkg.com/pdfjs-dist/cmaps/',
                url: doc,
            }" />
    </div>
</template>


<script setup>

import VuePdfEmbed, { useVuePdfEmbed } from 'vue-pdf-embed'
// essential styles
import 'vue-pdf-embed/dist/style/index.css'
// optional styles
import 'vue-pdf-embed/dist/style/annotationLayer.css'
import 'vue-pdf-embed/dist/style/textLayer.css'


const { doc } = useVuePdfEmbed({
  source: 'https://raw.githubusercontent.com/mozilla/pdf.js/ba2edeae/web/compressed.tracemonkey-pldi-09.pdf',
})


</script>


<style lang="scss">
.pdf-ctn{
    width: 100%;
    height: 100%;
    min-height: 90vh;
    min-width: 400px;
    background-color: lightgray;
}
</style>