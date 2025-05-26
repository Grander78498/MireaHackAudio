<script setup>
import play from '@/assets/svg/play.vue';
</script>

<template>
<div class="music-info-div">
    <button class="play-button">
        <play />
    </button>
    <div class="info-div">
        <h2>Название</h2>
        <h3>Автор</h3>
    </div>
    <div class="time-div">
        <p>9:05</p>
    </div>
</div>
</template>

<style scoped>
.music-info-div {
    width: 550px;
    height: 66px;
    background-color: #fff;
    border-radius: 20px;
    border: 1px solid #000;

    display: flex;
    flex-direction: row;
    align-items: center;
    position: relative;
    gap: 5px;
}

.play-button {
    width: 48px;
    height: 48px;
    border-radius: 24px;
    background-color: #482612;
    display: flex;
    align-items: center;
    justify-content: center;
}

.info-div h2, .info-div h3, .time-div p {
    font-family: Cormorant;
    font-size: 24px;
    font-weight: 400;
}

.info-div h2, .time-div p {
    color: #000;
}

.info-div h3 {
    color: #00000099;
}

.time-div {
    position: absolute;
    right: 13px;
}
</style>