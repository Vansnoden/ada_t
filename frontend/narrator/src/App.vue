<template>
  <v-app>
      <v-main class="main-page">
        <router-view></router-view>
      </v-main>
  </v-app>
</template>

<script setup>
  import {useUserStore} from "@/stores/UserStore";
  const user = useUserStore();
</script>

<style lang="scss">
.main-page{
  min-height: 80vh;
}
</style>