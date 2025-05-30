<script setup>
import { ref, useTemplateRef } from 'vue';

const props = defineProps({
  texts: {
    type: Array,
    default: () => [{ "word": "только", "start": 27.32, "end": 27.92 },
    { "word": "только", "start": 27.32, "end": 27.92 },
    { "word": "только", "start": 27.32, "end": 27.92 },
    { "word": "только", "start": 27.32, "end": 27.92 },
    { "word": "только", "start": 27.32, "end": 27.92 },
    { "word": "только", "start": 27.32, "end": 27.92 },
    { "word": "только", "start": 27.32, "end": 27.92 },
    { "word": "только", "start": 27.32, "end": 27.92 },
    { "word": "только", "start": 27.32, "end": 27.92 }
    ]
  }
})


const offset = ref(0)
const last_end = ref(0)
const isRunning = ref(false)
let intervalId = null

const startTimer = () => {
  if (offset.value >= props.texts.length - 2) return;

  const updateOffset = () => {
    if (offset.value >= props.texts.length - 2) {
      clearInterval(intervalId);
      return;
    }
    
    const currentIndex = offset.value;
    const nextIndex = offset.value + 1;
    last_end.value = props.texts[currentIndex].end;
    const delay = (props.texts[nextIndex].end - last_end.value) * 1000;
    
    offset.value = nextIndex;
    
    // Очищаем предыдущий интервал и устанавливаем новый
    clearInterval(intervalId);
    intervalId = setTimeout(updateOffset, delay);
  };

  // Начальный запуск
  intervalId = setTimeout(updateOffset, (props.texts[offset.value].end - last_end.value + 1) * 1000);
}

const stopTimer = () => {
  clearInterval(intervalId)
}

const toggleTimer = () => {
  console.log("Запуск таймера")
  isRunning.value = !isRunning.value
  isRunning.value ? startTimer() : stopTimer()
}

defineExpose({
  toggleTimer
})
</script>

<template>
  <div class="music-text-main-div" v-if="texts">
    <h3>{{ texts[offset].word }}</h3>
    <h2>{{ texts[1 + offset].word }}</h2>
    <h1>{{ texts[2 + offset].word }}</h1>
    <h2 v-if="offset < (texts.length - 1)">{{ texts[3 + offset].word }}</h2>
    <h3 v-if="offset < (texts.length - 2)">{{ texts[4 + offset].word }}</h3>
  </div>
</template>

<style>
.music-text-main-div {
  width: 660px;
  height: 548px;
  background-color: #fff;
  border-radius: 20px;
  border: 1px solid #000000;

  display: flex;
  flex-direction: column;
  text-align: center;
  justify-content: center;
  gap: 70px;
}

.music-text-main-div h1 {
  font-family: Cormorant;
  font-weight: 700;
  font-size: 48px;
  line-height: 100%;
  letter-spacing: 0%;
}

.music-text-main-div h2 {
  font-family: Cormorant;
  font-weight: 400;
  font-size: 40px;
  line-height: 100%;
  letter-spacing: 0%;
}

.music-text-main-div h3 {
  font-family: Cormorant;
  font-weight: 400;
  font-size: 38px;
  line-height: 100%;
  letter-spacing: 0%;
  color: #00000099;
}
</style>