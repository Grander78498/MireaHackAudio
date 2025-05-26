import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import LoadMusicPage from '@/views/LoadMusicPage.vue'
import RebuildMusic from '@/views/RebuildMusic.vue'


const routes = [
  { path: '/', component: Home },
  { path: '/musicload', component: LoadMusicPage}, 
  { path: '/rebuildmusic', component: RebuildMusic}, 

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router