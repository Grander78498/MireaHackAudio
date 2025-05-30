<script setup>
import strelka from '@/assets/svg/strelka.vue';
import MusicText from '@/components/MusicText.vue';
import play from '@/assets/svg/play.vue';

import { useRoute } from 'vue-router';
import { ref, useTemplateRef } from 'vue';
import axios from 'axios';

const route = useRoute();
const audioInfo = ref({
    original_file_name: '',
    cleaned_file_name: '',
    author: '',
    performer: '',
    year: 0,
    tags: ['tag1', 'tag2', 'tag3'],
    word_timestamps: null
});
const originalAudio = useTemplateRef('original-audio');
const cleanedAudio = useTemplateRef('cleaned-audio');
const originalMinutes = ref('0');
const originalSeconds = ref('00');
const cleanedMinutes = ref('0');
const cleanedSeconds = ref('00');
const current_minutes = ref('0');
const current_seconds = ref('00');
const progress = ref(0);


console.log(route.params.id);

const loadAudio = async (original) => {
    const audio = original ? originalAudio : cleanedAudio
    if ((original && !audioInfo.value.original_file_name)
        || (!original && !audioInfo.value.cleaned_file_name)) return

    if (audio.value.src) return
    try {
        const response = await fetch('http://127.0.0.1:8000/load', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                filename:
                    original
                        ? audioInfo.value.original_file_name
                        : audioInfo.value.cleaned_file_name
            })
        })

        if (!response.ok) throw new Error('Ошибка при получении аудио')

        const blob = await response.blob()
        const audioUrl = URL.createObjectURL(blob)

        audio.value.src = audioUrl
        audio.value.onloadedmetadata = () => {
            let duration = Math.floor(audio.value.duration);
            originalMinutes.value = (Math.floor(duration / 60)).toString();
            originalSeconds.value = (duration % 60).toString();
            cleanedMinutes.value = (Math.floor(duration / 60)).toString();
            cleanedSeconds.value = (duration % 60).toString();
        }
    }
    catch (err) {
        console.log('Ошибка при воспроизведении:', err)
    }
}

const loadMusicInfo = async () => {
    try {
        const response = await axios.get(`http://127.0.0.1:8000/audio/${route.params.id}`);

        audioInfo.value = response.data;

        await loadAudio(true)
        await loadAudio(false)

    } catch (error) {
        console.error('Ошибка загрузки:', error);
        alert('Произошла ошибка при загрузке');
    }
}

const playStreamedAudio = async (original) => {
    await loadAudio(original);
    
    if (original && originalAudio.value.paused) {
        await originalAudio.value.play()
        cleanedAudio.value.pause()
    }
    else if (original && !originalAudio.value.paused) {
        originalAudio.value.pause()
    }
    else if (!original && cleanedAudio.value.paused) {
        await cleanedAudio.value.play()
        originalAudio.value.pause()
    }
    else if (!original && !cleanedAudio.value.paused) {
        cleanedAudio.value.pause()
    }
}
const TextComp = useTemplateRef("TextComp");
const buttonPlayAudio = (original) => {
    playStreamedAudio(original);
    TextComp.value.toggleTimer()
}

loadMusicInfo();
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
                    <div class="music-info-div">
                        <button class="play-button" @click="() => buttonPlayAudio(true)">
                            <play />
                        </button>
                        <div class="info-div">
                            <h2>{{ audioInfo.original_file_name }}</h2>
                            <h3>{{ audioInfo.author }}</h3>
                        </div>
                        <div class="time-div">
                            <p>{{ originalMinutes.padStart(2, '0') }}:{{ originalSeconds.padStart(2, '0') }}</p>
                        </div>
                        <audio ref="original-audio"></audio>
                    </div>
                </div>
                <div class="music-inf-div">
                    <h1>Восстановленная версия</h1>
                    <div class="music-info-div">
                        <button class="play-button" @click="() => buttonPlayAudio(false)">
                            <play />
                        </button>
                        <div class="info-div">
                            <h2>{{ audioInfo.cleaned_file_name }}</h2>
                            <h3>{{ audioInfo.author }}</h3>
                        </div>
                        <div class="time-div">
                            <p>{{ cleanedMinutes.padStart(2, '0') }}:{{ cleanedSeconds.padStart(2, '0') }}</p>
                        </div>
                        <audio ref="cleaned-audio"></audio>
                    </div>
                </div>
                <div class="music-inf-div">
                    <h2>Тэги:</h2>
                    <div class="music-tag-div">
                        <div class="tag-div" v-for="tag in audioInfo.tags">
                            <p>{{ tag }}</p>
                        </div>
                    </div>
                </div>
                <div class="rebuild-music-button-div">
                    <a class="save-button" href="/editmusic">Сохранить</a>
                    <button class="change-button">Редактировать</button>
                </div>
            </div>
        </div>
        <div class="music-text-div">
            <MusicText ref="TextComp" :texts="audioInfo.word_timestamps" /> <!--Работает Егор! Не подходить!-->
            <div class="music-progress-bar">
                <p class="timer-div">{{ current_minutes }}:{{ current_seconds }}</p>
                <div class="progress-bar-div">
                    <div class="point-bar-div" :style="{ left: `${progress}%` }">
                    </div>
                </div>
                <p class="timer-div">{{ originalMinutes }}:{{ originalSeconds }}</p>
            </div>
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

.music-tag-div {
    display: flex;
    flex-direction: row;
    justify-content: center;
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
    display: flex;
    flex-direction: column;
    margin-left: 100px;
}

.music-tag-div {
    width: 550px;
    height: 50px;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 5px;
}

.tag-div {
    display: inline-block;
    height: 28px;
    border: 1px solid #000;
    background-color: #fff;
    border-radius: 20px;
    padding: 5px 10px;

    font-family: Cormorant;
    font-weight: 400;
    font-size: 20px;
    line-height: 100%;
    letter-spacing: 0%;
}

.progress-bar {
    width: 540px;
    height: 2px;
    background-color: #482612;
}

/*
|||||||||||||||||||||
||| MusicInfo.vue |||
|||||||||||||||||||||
*/

audio {
    display: none;
}

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

.info-div h2,
.info-div h3,
.time-div p {
    font-family: Cormorant;
    font-size: 24px;
    font-weight: 400;
}

.info-div h2,
.time-div p {
    color: #000;
}

.info-div h3 {
    color: #00000099;
}

.time-div {
    position: absolute;
    right: 13px;
    font-family: Cormorant;
    font-size: 24px;
    font-weight: 400;
    color: #000;
}

.timer-div {
    font-family: Cormorant;
    font-size: 20px;
    font-weight: 400;
    color: #000;
}

.music-progress-bar {
    position: relative;
    margin-top: 15px;
    width: 100%;
    height: 50px;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    gap: 5px;
    visibility: hidden;
}

.progress-bar-div {
    width: 540px;
    height: 5px;
    background-color: #482612;
}

.point-bar-div {
    top: 25px;
    width: 14px;
    height: 14px;
    background-color: #482612;
    border-radius: 14px;
    border: 1px solid #FFFCDF;

    position: absolute;
    
}
</style>