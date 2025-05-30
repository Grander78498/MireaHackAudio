// test-setup/TempMusicList.js
export default {
    template: `
      <div class="main-music-list-div">
        <div class="search-div">
          <input placeholder="Введите название песни или автора">
        </div>
        <div class="music-list-div">
          <div class="music-div" v-for="i in 5" :key="i">
            <div class="inf-div">
              <h1>Музыка {{i}}</h1>
            </div>
          </div>
        </div>
      </div>
    `
  }