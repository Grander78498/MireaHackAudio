<script setup>
import { ref, computed } from 'vue'
import MiniMusicPlayer from '../assets/svg/miniMusicPlayer.vue'
import SeachIcon from '../assets/svg/search.vue'
import FilterIcon from '../assets/svg/filter.vue'
import Filter from './Filter.vue'
import axios from 'axios'


const showFilter = ref(false)
const searchQuery = ref('')

const musics = ref({'result': []})

const loadMusics = async () => {
    const response = await axios.get('http://127.0.0.1:8000/audio')
    musics.value = response.data.result.slice(-3);
    console.log(musics.value)
}

loadMusics();

const filteredMusics = computed(() => {
  if (!searchQuery.value) return musics.value
  
  const query = searchQuery.value.toLowerCase()
  return musics.value.filter(music => {
    return music.original_file_name.toLowerCase().includes(query) || 
           music.author.toLowerCase().includes(query)
  })
})

const toggleFilter = () => {
  showFilter.value = !showFilter.value
}
</script>

<template>
<div class="main-music-list-div">
    <div class="search-div">
        <div class="svg1-div">
            <SeachIcon />
        </div>
        <input 
            v-model="searchQuery" 
            placeholder="Введите название песни или автора"
        >
        <button @click="search">Найти</button>
        <div class="svg2-div" @click="toggleFilter">
            <FilterIcon />
        </div>
    </div>
    
    <Filter 
      v-if="showFilter" 
      @close="showFilter = false" 
      class="music-filter-div-absolute"
    />
    <div class="music-list-div" role="list">
        <div class="music-div" v-for="music in filteredMusics" :key="music" role="listitem">
            <div class="img-div">
                <div class="first-img-rec-div">
                    <div class="second-img-rec-div">
                        <MiniMusicPlayer />
                    </div>
                </div>
            </div>
            <div class="inf-div">
                <h1>{{ music.original_file_name }}</h1>
                <div>
                    <h2>{{ music.author }}</h2>
                </div>
            </div>
            <!-- <div class="time-div">
                <p>{{ music.time }}</p>
            </div> -->
        </div>
        <div v-if="filteredMusics.length === 0" class="no-results">
            Ничего не найдено
        </div>
    </div>
</div>
</template>

<style scoped>
.main-music-list-div {
    margin-top: 40px;
    width: 90%;
    margin-bottom: 75px;
}

.first-img-rec-div {
    width: 66px;
    height: 66px;
    border-radius: 8px;
    background-color: #000;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 0;
}

.second-img-rec-div {
    width: 44px;
    height: 44px;
    border-radius: 8px;
    background-color: #000;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1;
}

.music-div {
    width: 100%;
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 15px;
}

.music-div:not(:last-child)  {
    padding-bottom: 15px;
    border-bottom: 1px solid #000;
}

.music-list-div {
    margin-top: 60px;
    gap: 15px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.music-div h1 {
    font-family: Cormorant;
    font-size: 24px;
    font-weight: 400;
    color: #000;
}

.music-div h2 { 
    font-family: Cormorant;
    font-size: 24px;
    font-weight: 400;
    color: #00000099;
}

.time-div {
    margin-left: auto;
}

.search-div {
    display: flex;
    flex-direction: row;
    position: relative;
    align-items: center;
    width: 100%;
}

.search-div button {
    width: 150px;
    height: 40px;
    background-color: #482612;
    border-radius: 35px;
    right: 85px;
    font-family: Cormorant;
    font-size: 24px;
    font-weight: 400;
    color: #FFF;
    position: absolute;
    cursor: pointer;
}

.search-div input {
    position: relative;
    width: 100%;
    height: 55px;
    border-radius: 35px;
    border: 1px solid #000;
    background-color: #FFF;
    padding-left: 65px;
    font-family: Cormorant;
    font-size: 24px;
    font-weight: 400;
    color: #00000080;
}

.svg1-div {
    position: absolute;
    z-index: 100;
    left: 15px;
    height: 26px;
}

.svg2-div {
    position: absolute;
    z-index: 100;
    right: 30px;
    height: 26px;
}

.no-results {
    font-family: Cormorant;
    font-size: 24px;
    color: #00000080;
    padding: 20px;
}

.music-filter-div-absolute {
    position: absolute;
    z-index: 100;
    right: 65px;
    margin-top: 20px;
}
</style>