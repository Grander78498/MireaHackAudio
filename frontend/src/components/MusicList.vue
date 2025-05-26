<script>
export default {
    data() {
        return {
            musics: [
                {name: 'Музыка 1', authors: ['Автор11', 'Автор21'], time: "2:02"},
                {name: 'Музыка 2', authors: ['Автор12', 'Автор22'], time: "9:05"},
                {name: 'Музыка 3', authors: ['Автор13', 'Автор23'], time: "22:06"},
                {name: 'Музыка 4', authors: ['Автор14', 'Автор24'], time: "28:04"},
                {name: 'Музыка 5', authors: ['Автор15', 'Автор25'], time: "10:05"}
            ],
            searchQuery: ''
        }
    },
    computed: {
        filteredMusics() {
            if (!this.searchQuery) return this.musics;
            
            const query = this.searchQuery.toLowerCase();
            return this.musics.filter(music => {
                const nameMatch = music.name.toLowerCase().includes(query);
                const authorsMatch = music.authors.some(author => 
                    author.toLowerCase().includes(query)
                );
                return nameMatch || authorsMatch;
            });
        }
    },
   methods: {
  search() {
    if (!this.searchQuery) {
      this.filteredMusics = [...this.musics];
      return;
    }
    
    const query = this.searchQuery.toLowerCase();
    this.filteredMusics = this.musics.filter(music => {
      return music.name.toLowerCase().includes(query) || 
             music.authors.some(author => author.toLowerCase().includes(query));
    });
  },

},
mounted() {
  this.search(); // инициализация при загрузке
}
}
</script>

<script setup>
    import MiniMusicPlayer from '../assets/svg/miniMusicPlayer.vue';
    import MusicPlayer from '../assets/svg/musicPlayer.vue';
    import SeachIcon from '../assets/svg/search.vue';
    import FilterIcon from '../assets/svg/filter.vue';
    import Filter from './Filter.vue';
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
            @input="search"
        >
        <button @click="search">Найти</button>
        <div class="svg2-div">
            <FilterIcon />
        </div>
    </div>
    <div class="music-filter-div-absolute">
        <Filter />
    </div>
    <div class="music-list-div">
        <div class="music-div" v-for="music in filteredMusics" :key="music.name">
            <div class="img-div">
                <div class="first-img-rec-div">
                    <div class="second-img-rec-div">
                        <MiniMusicPlayer />
                    </div>
                </div>
            </div>
            <div class="inf-div">
                <h1>{{ music.name }}</h1>
                <div>
                    <h2>{{ music.authors.join(', ') }}</h2>
                </div>
            </div>
            <div class="time-div">
                <p>{{ music.time }}</p>
            </div>
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