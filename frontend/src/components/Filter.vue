<script setup>
import { ref } from 'vue';
import cross from '@/assets/svg/cross.vue';
import strelka2 from '@/assets/svg/strelka2.vue';
import AuthorList from './Lists/AuthorList.vue';
import PerformersList from './Lists/PerformersList.vue';

const emit = defineEmits(['close'])

const showAuthors = ref(false);
const showPerformers = ref(false);

function toggleList(listName) {
  if (listName === 'authors') {
    showAuthors.value = !showAuthors.value;
  } else if (listName === 'performers') {
    showPerformers.value = !showPerformers.value;
  }
}
</script>

<template>
  <div class="filter-main-div">
    <div class="header-div">
      <h1>Фильтр</h1>
      <cross @click="emit('close')" />
    </div>

    <!-- Автор -->
    <div class="filter-select-div">
      <h2>Автор</h2>
      <div class="select-input-div">
        <input>
        <div
          class="filer-strelka-div"
          :class="{ rotated: showAuthors }"
          @click="toggleList('authors')"
        >
          <strelka2 />
        </div>
      </div>
      <transition name="expand">
        <div
          class="author-list-div expandable"
          v-show="showAuthors"
        >
          <AuthorList />
        </div>
      </transition>
    </div>

    <!-- Исполнитель -->
    <div class="filter-select-div">
      <h2>Исполнитель</h2>
      <div class="select-input-div">
        <input>
        <div
          class="filer-strelka-div"
          :class="{ rotated: showPerformers }"
          @click="toggleList('performers')"
        >
          <strelka2 />
        </div>
      </div>
      <transition name="expand">
        <div
          class="performer-list-div expandable"
          v-show="showPerformers"
        >
          <PerformersList />
        </div>
      </transition>
    </div>

    <!-- Год -->
    <div class="filter-year-div">
      <h2>Год</h2>
      <input>
    </div>
  </div>
</template>


<style scoped>
.filter-main-div {
    width: 847px;
    height: 367px;
    background-color: #fff;
    border-radius: 20px;
    border: 1px solid #000;

    display: flex;
    flex-direction: column;
    gap: 15px;

    padding-left: 30px;
    padding-top: 20px;
    padding-bottom: 54px;
}

.filter-main-div h1 {
    font-family: Cormorant;
    font-size: 32px;
    font-weight: 400;
    color: #000;
}

.header-div {
    display: flex;
    flex-direction: row;
    gap: 668px;
}

.filter-select-div h2, .filter-year-div h2 {
    font-family: Cormorant;
    font-size: 28px;
    font-weight: 400;
    color: #000;
}

.filter-select-div input, .filter-year-div input {
    width: 435px;
    height: 30px;
    background-color: #fff;
    border-radius: 20px;
    border: 1px solid #000;
    padding-left: 15px;

    font-family: Cormorant;
    font-size: 24px;
    font-weight: 400;
    color: #000;
}

.filter-select-div {
    width: 435px;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.select-input-div {
    position: relative;
}

.filer-strelka-div {
    position: absolute;
    right: 5px;
    top: 10px;
}
</style>