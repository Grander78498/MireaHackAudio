<script setup>
    import music from '@/assets/svg/music.vue';
</script>

<template>
        <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant:ital,wght@0,300..700;1,300..700&display=swap" rel="stylesheet">
<div class="main-header-div">
    <div class="icon-div">
        <music />
    </div>
    <div class="search-div">
        <a>Поиск</a>
    </div>
</div>
</template>

<style scoped>
.main-header-div {
    width: 100%;
    height: 50px;
    background-color: #FFF;

    display: flex;
    flex-direction: row;
    align-items: center;
    position: relative;

    font-family: Cormorant;
    font-size: 24px;
    font-weight: 400;
    color: #000;
}

.icon-div {
    position: absolute;
    left: 20px;
}

.search-div {
    position: absolute;
    left: 50%;
}
</style>