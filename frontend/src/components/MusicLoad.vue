<script setup>
import Skrepka from '@/assets/svg/skrepka.vue';
import { ref } from 'vue';

const fileInput = ref(null);
const audioFile = ref(null);
const fileName = ref("");
const audioUrl = ref("");
const text_file = ref("");

const triggerFileInput = () => {
  fileInput.value.click();
};

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (!file) return;
  
  if (!file.type.match('audio.*')) {
    return;
  }
  
  audioFile.value = file;
  fileName.value = file.name;
  text_file.value = file.name;
  audioUrl.value = URL.createObjectURL(file);
};

const removeFile = () => {
  audioFile.value = null;
  fileName.value = "";
  text_file.value = "";
  audioUrl.value = "";
  fileInput.value.value = "";
};
</script>

<template>
  <div class="main-music-load-div">
    <div class="audio-load-div">
      <h2>Загрузите аудио</h2>
      <input type="file" ref="fileInput"accept="audio/*"@change="handleFileUpload"class="hidden-input">
      <div class="music-load-div" @click="triggerFileInput">
        <div class="upload-div">
          <Skrepka />
          <p>{{ text_file || "Загрузите файл" }}</p>
          <button class="select-btn"></button>
        </div>
      </div>
    </div>
    
    <div class="text-input-div">
      <h2>Автор</h2>
      <input>
    </div>
    
    <div class="text-input-div">
      <h2>Исполнитель</h2>
      <input>
    </div>
    
    <div class="text-input-div">
      <h2>Год</h2>
      <input type="number">
    </div>
    <div class="button-div">
        <button>Загрузить запись</button>
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

.button-div button {
    width: 285px;
    height: 50px;
    border-radius: 35px;
    background-color: #482612;
    align-items: center;

    font-family: Cormorant;
    font-size: 24px;
    font-weight: 400;
    color: #fff;
}

.button-div {
    margin-top: 60px;
    cursor: pointer;
}

</style>