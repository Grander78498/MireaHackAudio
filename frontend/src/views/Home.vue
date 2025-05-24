<script setup>
import LoadMusic from '@/components/LoadMusic.vue';
import MusicList from '@/components/MusicList.vue';
</script>

<template>
<div class="main-div">
    <LoadMusic />
    <div class="music-list-div">
        <MusicList />
    </div>
</div>
</template>

<style scoped>
.main-div {
    background-color: #FFFFF2;
}

.music-list-div {
    display: flex;
    justify-content: center;
    width: 100%;
}
</style>