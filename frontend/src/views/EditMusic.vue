<script setup>
import strelka from '@/assets/svg/strelka.vue';
</script>

<template>
<div class="edit-music-page-main-div">
    <strelka />
    <h2 style="margin-top: 14px;">Редактировать</h2>
    <div class="edit-text-div">
        <div class="edit-textarea-div">
            <h2>Текст</h2>
            <textarea></textarea>
        </div>
        <div class="edit-input-div">
            <h2>Автор</h2>
            <input>
        </div>
        <div class="edit-input-div">
            <h2>Исполнитель</h2>
            <input>
        </div>
        <div class="edit-input-div">
            <h2>Год</h2>
            <input>
        </div>
        <div class="edit-button-div">
            <button>Сохранить</button>
        </div>
    </div>
</div>
</template>

<style>
.edit-music-page-main-div {
    padding-top: 37px;
    padding-bottom: 128px;
    padding-left: 60px;
    padding-right: 60px;
}

.edit-text-div {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 17px;
}

h2 {
    font-family: Cormorant;
    font-weight: 400;
    font-size: 36px;
    line-height: 100%;
    letter-spacing: 0%;
    color: #000;
}

.edit-textarea-div textarea {
    width: 435px;
    height: 411px;
    border-radius: 20px;
    border: 1px solid #000000;
    resize: none;
    margin-top: 12px;
}

.edit-input-div {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-top: 30px;
}

.edit-input-div input {
    width: 435px;
    height: 45px;
    border-radius: 35px;
    background-color: #fff;
    border: 1px solid #000000;
    margin-top: 12px;
}

.edit-button-div button {
    width: 284px;
    height: 51px;
    border-radius: 35px;
    background-color: #482612;

    font-family: Cormorant;
    font-weight: 400;
    font-size: 24px;
    line-height: 100%;
    letter-spacing: 0%;
    color: #fff;

    margin-top: 160px;
    display: flex;
    align-items: center;
    justify-content: center;
}
</style>