import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import LoadMusicPage from '@/views/LoadMusicPage.vue'
import RebuildMusic from '@/views/RebuildMusic.vue'
import EditMusic from '@/views/EditMusic.vue'
import PlayMusic from '@/views/PlayMusic.vue'


const routes = [
  { path: '/', component: Home },
  { path: '/musicload', component: LoadMusicPage}, 
  { path: '/rebuildmusic/:id', component: RebuildMusic}, 
  { path: '/editmusic', component: EditMusic},
  { path: '/testStream', component: PlayMusic}
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router