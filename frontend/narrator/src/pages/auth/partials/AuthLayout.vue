<template>
    <v-layout>
        <div class="auth-ctn">
            <slot name="content"></slot>
        </div>
    </v-layout>
</template>

<script>
export default{
    mounted(){

    }
}
</script>

<style lang="scss">
.auth-ctn{
    box-sizing: border-box;
    background-image: url('@/assets/auth-bg.jpg');
    background-size: cover;
    background-repeat: no-repeat;
    height: 100vh;
    width: 100vw;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
}
</style>