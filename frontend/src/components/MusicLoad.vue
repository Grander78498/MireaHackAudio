<script setup>
import Skrepka from '@/assets/svg/skrepka.vue';
import axios from 'axios';
import { ref } from 'vue';
import { musicIndexStore } from '@/stores/store';
import router from '@/router';

const fileInput = ref(null);
const file = ref(null);
const author = ref('');
const performer = ref('');
const year = ref('');
const isLoading = ref(false);
const audioFile = ref(null);
const fileName = ref("");
const store = musicIndexStore();

function triggerFileInput() {
  fileInput.value.click();
}
function handleFileUpload(event) {
  const inputFile = event.target.files[0];
  if (!inputFile) return;
  
  if (!inputFile.type.match('audio.*')) {
    alert('Пожалуйста, выберите аудиофайл');
    return;
  }
  
  file.value = inputFile;
  fileName.value = inputFile.name;
}
async function uploadMusic() {
  if (!file.value) {
    alert('Пожалуйста, выберите аудиофайл');
    return;
  }

  isLoading.value = true;
  
  const formData = new FormData();
  formData.append('file', file.value);
  formData.append('author', author.value);
  formData.append('performer', performer.value);
  formData.append('year', year.value);
  
  try {
    const response = await axios.post('http://127.0.0.1:8000/save', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    if (response.data && response.data.id) {
      store.setMusicIndex(response.data.id.toString())
      console.log(`${response.data.id}`)
    }
    
    // Обработка успешной загрузки
    alert('Музыка успешно загружена!');
    resetForm();

    router.push({ path: `/rebuildmusic/${response.data.id.toString()}`});
  } catch (error) {
    console.error('Ошибка загрузки:', error);
    alert('Произошла ошибка при загрузке');
  } finally {
    isLoading.value = false;
  }
}
function resetForm() {
  file.value = null;
  fileName.value = '';
  author.value = '';
  performer.value = '';
  year.value = '';
  fileInput.value = '';
}
</script>

<!-- <script>


export default {
  data() {
    return {
      file: null,
      file_name: '',
      author: '',
      performer: '',
      year: '',
      isLoading: false,
    }
  },
  methods: {
    resetForm() {
      this.file = null;
      this.file_name = '';
      this.author = '';
      this.performer = '';
      this.year = '';
      this.$refs.fileInput.value = '';
    }
  }
}
</script> -->

<template>
  <div class="main-music-load-div">
    <div class="audio-load-div">
      <h2>Загрузите аудио</h2>
      <input 
        type="file" 
        ref="fileInput"
        accept="audio/*"
        @change="handleFileUpload"
        class="hidden-input"
      >
      <div class="music-load-div" @click="triggerFileInput">
        <div class="upload-div">
          <Skrepka />
          <p v-if="!fileName">Загрузите файл</p>
          <p v-else>{{ fileName }}</p>
        </div>
      </div>
    </div>
    
    <div class="text-input-div">
      <h2>Автор</h2>
      <input v-model="author" placeholder="Введите автора">
    </div>
    
    <div class="text-input-div">
      <h2>Исполнитель</h2>
      <input v-model="performer" placeholder="Введите исполнителя">
    </div>
    
    <div class="text-input-div">
      <h2>Год</h2>
      <input type="number" v-model="year" placeholder="Введите год">
    </div>
    
    <div class="button-div">
      <a @click="uploadMusic" :disabled="isLoading">
        {{ isLoading ? 'Загрузка...' : 'Загрузить запись' }}
      </a>
    </div>
  </div>
</template>

<style>
.main-music-load-div {
    width: 610px;
    height: 700px;
    background-color: #fff;
    border: 1px solid black;
    border-radius: 20px;

    display: flex;
        flex-direction: column;
    align-items: center;
    margin-top: 80px;
    margin-bottom: 200px;
}

.audio-load-div, .text-input-div {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.audio-load-div h2, .text-input-div h2 {
  font-family: Cormorant;
  font-size: 36px;
  font-weight: 400;
  color: #000;
  margin-bottom: 10px;
}

.audio-load-div {
    margin-top: 50px;
}

.text-input-div {
    margin-top: 20px;
}


.music-load-div {
  width: 490px;
  height: 45px;
  background-color: #fff;
  border: 1px solid #000;
  border-radius: 35px;
  position: relative;
  display: flex;
  align-items: center;
  cursor: pointer;
}

.upload-div {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 15px;
  margin-left: 16px;
  width: 100%;
}

.upload-div p {
  font-family: Cormorant;
  font-size: 24px;
  font-weight: 400;
  color: #00000080;
  flex-grow: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.select-btn {
  background: transparent;
  border: none;
  font-family: Cormorant;
  font-size: 24px;
  font-weight: 400;
  color: #000;
  cursor: pointer;
  padding-right: 20px;
}

.hidden-input {
  display: none;
}

.text-input-div input {
  width: 490px;
  height: 45px;
  background-color: #fff;
  border: 1px solid #000;
  border-radius: 35px;
  font-family: Cormorant;
  font-size: 20px;
}

.button-div a {
    width: 285px;
    height: 50px;
    border-radius: 35px;
    background-color: #482612;
    align-items: center;

    font-family: Cormorant;
    font-size: 24px;
    font-weight: 400;
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    text-decoration: none;
}

.button-div {
    margin-top: 60px;
    cursor: pointer;
}

.button-div button {
  width: 285px;
  height: 50px;
  border-radius: 35px;
  background-color: #482612;
  border: none;
  color: #fff;
  font-family: Cormorant;
  font-size: 24px;
  font-weight: 400;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.button-div button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

</style>
