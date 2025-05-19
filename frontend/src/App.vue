<script setup>
  import Header_1 from './components/Header.vue';
  import Footer_1 from './components/Footer.vue'
</script>

<template>
<div class="app"></div>
<Header_1 />
<main>
      <router-view></router-view>
</main>
<Footer_1 />
</template>

<style>
.app {
  display: flex;
  flex-direction: column;
}
main {
  flex: 1;
  background-color: #FFFFF2;
}
</style>
