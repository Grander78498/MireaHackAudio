import { mount } from '@vue/test-utils'
import LoadMusic from '@/components/LoadMusic.vue'
import { describe, it, expect } from 'vitest'

describe('LoadMusic.vue', () => {
    const MusicPlayerMock = { template: '<div class="mock-player"></div>' }
  
    it('рендерит базовую структуру', () => {
      const wrapper = mount(LoadMusic, {
        global: {
          stubs: {
            MusicPlayer: MusicPlayerMock
          }
        }
      })
  

      expect(wrapper.find('h1').text()).toBe('Записи военных лет')
      expect(wrapper.findAll('p').length).toBe(2)
      expect(wrapper.find('a').text()).toBe('Загрузить запись')
      expect(wrapper.find('.mock-player').exists()).toBe(true)
    })
  
    it('ссылка имеет правильный атрибут href', () => {
      const wrapper = mount(LoadMusic)
      expect(wrapper.find('a').attributes('href')).toBe('/musicload')
    })
  })