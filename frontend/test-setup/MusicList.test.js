import { mount } from '@vue/test-utils'
import MusicList from '../src/components/MusicList.vue'
import { describe, it, expect } from 'vitest'

describe('MusicList.vue', () => {
  it('проверка структуры компонента', () => {
    expect(MusicList.setup).toBeDefined()
  })
  it('базовый рендеринг компонента', async () => {
    const wrapper = mount(MusicList, {
      global: {
        stubs: {
          MiniMusicPlayer: { template: '<div class="mock-player"></div>' },
          SeachIcon: { template: '<div class="mock-search"></div>' },
          FilterIcon: { template: '<div class="mock-filter"></div>' },
          Filter: { template: '<div class="mock-filter-comp"></div>' }
        }
      }
    })

    await new Promise(resolve => setTimeout(resolve, 50))
    expect(wrapper.find('div').exists()).toBe(true)
    expect(wrapper.find('input').exists()).toBe(true)
  })

  it('проверка данных компонента', async () => {
    const wrapper = mount(MusicList)
    
    expect(wrapper.vm.searchQuery).toBe('')
    expect(wrapper.vm.musics.length).toBe(5)
    expect(wrapper.vm.filteredMusics.length).toBe(5)
    
    expect(typeof wrapper.vm.toggleFilter).toBe('function')
  })
})