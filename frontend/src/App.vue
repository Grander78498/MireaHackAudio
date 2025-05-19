<script setup>
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
}
</style>
