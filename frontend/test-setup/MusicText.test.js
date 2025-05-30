import { mount } from '@vue/test-utils'
import MusicText from '@/components/MusicText.vue'
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'

describe('MusicText.vue', () => {
  const mockTexts = [
    { word: "первое", start: 1.0, end: 1.5 },
    { word: "второе", start: 1.5, end: 2.0 },
    { word: "третье", start: 2.0, end: 2.5 },
    { word: "второе", start: 2.5, end: 3.0 },
    { word: "пятое", start: 3.0, end: 3.5 },
    { word: "шестое", start: 3.5, end: 4.0 }
  ]
  let wrapper = null
  beforeEach(async () => {
    vi.useFakeTimers()
    wrapper = mount(MusicText, {
      props: {
        texts: mockTexts
      }
    })
    await wrapper.vm.$nextTick()
  })
  afterEach(() => {
    if (wrapper) {
      wrapper.unmount()
    }
    vi.clearAllTimers()
    vi.restoreAllMocks()
  })
  it('получает и отображает начальные слова', async () => {
    expect(wrapper.props('texts')).toEqual(mockTexts)
    
    const h3Elements = wrapper.findAll('h3')
    const h2Elements = wrapper.findAll('h2')
    const h1Element = wrapper.find('h1')
  
    expect(h1Element.text()).toBe(mockTexts[2].word)
    expect(h2Elements[0].text()).toBe(mockTexts[3].word)
  })

  it('корректно инициализирует данные', () => {
    expect(wrapper.vm.offset).toBe(0)
    expect(wrapper.vm.isRunning).toBe(false)
    expect(wrapper.vm.last_end).toBe(0)
  })
  it('переключает состояние таймера', async () => {
    expect(wrapper.vm.isRunning).toBe(false)
    await wrapper.vm.toggleTimer()
    expect(wrapper.vm.isRunning).toBe(true)
    await wrapper.vm.toggleTimer()
    expect(wrapper.vm.isRunning).toBe(false)
  })

  it('имеет правильную структуру DOM', () => {
    expect(wrapper.find('.music-text-main-div').exists()).toBe(true)
    expect(wrapper.find('h1').exists()).toBe(true)
    expect(wrapper.find('h2').exists()).toBe(true)
    expect(wrapper.find('h3').exists()).toBe(true)
  })

  it('переключает слова по таймеру', async () => {
    await wrapper.vm.toggleTimer()
    expect(wrapper.vm.isRunning).toBe(true)
    vi.advanceTimersByTime(2500)
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.offset).toBe(1)
    expect(wrapper.find('h1').text()).toBe(mockTexts[3].word)
  })
})