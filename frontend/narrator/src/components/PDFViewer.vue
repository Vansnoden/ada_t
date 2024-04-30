<template>
    <div class="pdf-ctn">
        <div class="header">
            <span>PDF viewer</span>
            <v-btn ref="prev" text="Previous" @click="onPrevPage"/>
            <v-btn ref="next" text="Next" @click="onNextPage"/>
            &nbsp; &nbsp;
            <span>Page: <span ref="page_num"></span> / <span ref="page_count"></span></span>
        </div>
        <canvas ref="canvas"></canvas>
    </div>
</template>


<script setup>

import { ref, onMounted  } from 'vue';
/* @vite-ignore */
import '@/assets/pdfjs-4.2.67-dist/build/pdf.mjs';


// If absolute URL from the remote server is provided, configure the CORS
// header on that server.
const url = 'https://raw.githubusercontent.com/mozilla/pdf.js/ba2edeae/web/compressed.tracemonkey-pldi-09.pdf';

// Loaded via <script> tag, create shortcut to access PDF.js exports.
const { pdfjsLib } = globalThis;

// The workerSrc property shall be specified.
pdfjsLib.GlobalWorkerOptions.workerSrc = '/src/assets/pdfjs-4.2.67-dist/build/pdf.worker.mjs';


const canvas = ref(null);
const page_num = ref(null);
const page_count = ref(null);
const prev = ref(null);
const next = ref(null);
var pdfDoc = null;
var pageRendering = false;
var pageNumPending = null;
var scale = 1.4;
var ctx = null; 
var pageNum = 1;

/**
 * Get page info from document, resize canvas accordingly, and render page.
 * @param num Page number.
 */
function renderPage(num) {
    
    pageRendering = true;
    // Using promise to fetch the page
    pdfDoc.getPage(num).then(function(page) {
        var viewport = page.getViewport({scale: scale});
        canvas.value.height = viewport.height;
        canvas.value.width = viewport.width;

      // Render PDF page into canvas context
        var renderContext = {
            canvasContext: ctx,
            viewport: viewport
        };
        var renderTask = page.render(renderContext);

      // Wait for rendering to finish
        renderTask.promise.then(function() {
            pageRendering = false;
            if (pageNumPending !== null) {
                // New page rendering is pending
                renderPage(pageNumPending);
                pageNumPending = null;
            }
        });
    });
    // Update page counters
    page_num.value.textContent = num;
}

/**
 * If another page rendering in progress, waits until the rendering is
 * finised. Otherwise, executes rendering immediately.
 */
function queueRenderPage(num) {
    if (pageRendering) {
    pageNumPending = num;
    } else {
        renderPage(num);
    }
}

/**
 * Displays previous page.
 */
function onPrevPage() {
    if (pageNum <= 1) {
        return;
    }
    pageNum--;
    queueRenderPage(pageNum);
}



/**
 * Displays next page.
 */
function onNextPage() {
    if (pageNum >= pdfDoc.numPages) {
        return;
    }
    pageNum++;
    queueRenderPage(pageNum);
}

/**
 * Asynchronously downloads PDF.
 */
pdfjsLib.getDocument(url).promise.then(function(pdfDoc_) {
    pdfDoc = pdfDoc_;
    page_count.value.textContent = pdfDoc.numPages;
    // Initial/first page rendering
    renderPage(pageNum);
});


onMounted(() => {
    ctx = canvas.value.getContext('2d'); 
})

</script>


<style lang="scss">
.pdf-ctn{
    width: 100%;
    height: 100%;
    min-height: 90vh;
    min-width: 400px;
    background-color: lightgray;
    overflow-y: scroll;
    overflow-x: scroll;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    #the-canvas{
        width: 100%;
        height: 100%;
    }
    .header{
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: row;
        gap: 1em;
        width: 100%;
        background-color: beige;
        padding-top: 0.5em;
        padding-bottom: 0.5em;
    }
}
</style>