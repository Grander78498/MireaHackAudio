<script setup>
    import MusicInfo from '@/components/MusicInfo.vue';
    import strelka from '@/assets/svg/strelka.vue';
    import MusicText from '@/components/MusicText.vue';
</script>

<script>
import { musicIndexStore } from '@/stores/store';
import { storeToRefs } from 'pinia';

const indexStore = musicIndexStore()
const { index } = storeToRefs(musicIndexStore)
</script>

<template>
<div class="main-rebuild-music-div">
    <div class="left-div">
        <div class="strelka-div">
            <strelka />
        </div>
        <div class="music-div">
            <div class="music-inf-div">
                <h1>Оригинальная версия</h1>
                <MusicInfo />
            </div>
            <div class="music-inf-div">
                <h1>Восстановленная версия</h1>
                <MusicInfo />
            </div>
            <div class="rebuild-music-button-div">
                <a class="save-button" href="/editmusic">Сохранить</a>
                <button class="change-button">Редактировать</button>
            </div>
        </div>
    </div>
    <div class="music-text-div">
        <MusicText />
    </div>
</div>
</template>

<style scoped>
.main-rebuild-music-div {
    margin-left: 60px;
    margin-right: 60px;
    padding-top: 41px;
    padding-bottom: 100px;

    display: flex;
    flex-direction: row;
    justify-content: center
}

.left-div {
    display: flex;
    flex-direction: column;
}

.music-div {
    margin-top: 20px;
    width: 550px;
    display: flex;
    flex-direction: column;
    gap: 60px;
    margin-top: 20px;
}
.music-inf-div {
    display: flex;
    flex-direction: column;
    gap: 20px;
}
.music-inf-div h1 {
    font-family: Cormorant;
    font-weight: 400;
    font-size: 36px;
}

.rebuild-music-button-div {
    display: flex;
    flex-direction: column;
    gap: 20px;
    justify-content: center;
    align-items: center;
    margin-top: 90px;
}

.rebuild-music-button-div button {
    width: 284px;
    height: 51px;
    border-radius: 35px;

    font-family: Cormorant;
    font-weight: 400;
    font-size: 24px;
    line-height: 100%;
    letter-spacing: 0%;

    display: flex;
    align-items: center;
    justify-content: center;
}

.rebuild-music-button-div a {
    width: 284px;
    height: 51px;
    border-radius: 35px;

    font-family: Cormorant;
    font-weight: 400;
    font-size: 24px;
    line-height: 100%;
    letter-spacing: 0%;

    display: flex;
    align-items: center;
    justify-content: center;
    text-decoration: none;
}

.save-button {
    background-color: #482612;
    color: #fff;
}

.change-button {
    background-color: #fff;
    color: #000;
    border: 1px solid #000000
}

.music-text-div {
    margin-left: 100px;
}
</style>