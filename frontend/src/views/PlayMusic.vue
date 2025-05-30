<template>
  <div class="p-4">
    <input v-model="filename" placeholder="Введите имя MP3 файла" class="p-2 border rounded w-full mb-2" />
    <button @click="playStreamedAudio" class="px-4 py-2 bg-green-600 text-white rounded w-full">
      ▶️ Воспроизвести MP3
    </button>
    <audio ref="audio" controls class="mt-4 w-full" />
  </div>
</template>

<script setup>
import { ref, useTemplateRef } from 'vue'

const audio = useTemplateRef('audio');
const filename = ref('')

const playStreamedAudio = async () => {
  if (!filename.value || !audio.value) return

  try {
    const response = await fetch('http://127.0.0.1:8000/load', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ filename: filename.value })
    })

    if (!response.ok) throw new Error('Ошибка при получении аудио')

    const blob = await response.blob()
    const audioUrl = URL.createObjectURL(blob)

    audio.value.src = audioUrl
    audio.value.onloadedmetadata = () => {
      console.log(audio.value.duration);
    }
    await audio.value.play()
  } catch (err) {
    console.error('Ошибка при воспроизведении:', err)
  }
}
</script>

<style scoped>
input, button {
  font-size: 16px;
}
</style>
