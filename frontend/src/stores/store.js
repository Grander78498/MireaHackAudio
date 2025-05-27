import { defineStore } from "pinia";

export const musicIndexStore = defineStore('main', {
    state: () => ({
        musicIndex: ''
    }),
    actions: {
        setMusicIndex(value) {
            this.musicIndex = value
        }
    }
})