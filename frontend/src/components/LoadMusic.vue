<script setup>
    import MusicPlayer from '../assets/svg/musicPlayer.vue';
</script>

<template>
<div class="load-music-main-div">
    <div class="head-div">
        <h1>Записи военных лет</h1>
    </div>
    <div class="text-div">
        <p>Сервис реставрации</p>
        <p>любимых сердцу песен</p>
    </div>
    <div class="button-div">
        <button>Загрузить запись</button>
    </div>
    <div class="music-player-div">
        <MusicPlayer />
    </div>
</div>
</template>

<style scoped>
.load-music-main-div {
    width: 100%;
    height: 810px;
    background-image: url(../assets/img/main_image.jpg);
    position: relative;
}

h1 {
    font-family: Cormorant;
    font-size: 128px;
    font-weight: 400;
    color: #FFF;
}

.head-div {
    margin-top: 23px;
    margin-left: 76px;
}

p {
    font-family: Cormorant;
    font-size: 36px;
    font-weight: 400;
    color: #FFF;
}

.text-div {
    margin-left: 76px;
}

button {
    width: 340px;
    height: 60px;
    border-radius: 35px;
    background-color: #FFF;

    font-family: Cormorant;
    font-size: 32px;
    font-weight: 400;
    color: #000;
}

.button-div {
    margin-top: 100px;
    margin-left: 76px;
}

.music-player-div {
    position: absolute;
    bottom: 0px;
    right: 60px;
}
</style>