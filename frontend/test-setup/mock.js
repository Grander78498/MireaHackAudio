import { config } from '@vue/test-utils'

// Моки для всех SVG компонентов
const svgMocks = {
  MiniMusicPlayer: { template: '<div class="mock-player"></div>' },
  SeachIcon: { template: '<div class="mock-search"></div>' },
  FilterIcon: { template: '<div class="mock-filter"></div>' },
  Filter: { template: '<div class="mock-filter-comp"></div>' }
}

config.global.stubs = svgMocks