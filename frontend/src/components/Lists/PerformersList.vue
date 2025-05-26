<script>
export default {
    data() {
        return {
            performers : [
                'Исполнитель1',
                'Исполнитель2',
                'Исполнитель3',
                'Исполнитель4',
                'Исполнитель5',
                'Исполнитель6',
                'Исполнитель7',
                'Исполнитель8',
                'Исполнитель9',
                'Исполнитель10',
                'Исполнитель11',
                'Исполнитель12',
            ]
        }
    }
}
</script>

<template>
<div class="performers-list-div">
    <div v-for="performer in this.performers" class="performers-div">
        <p>{{ performer }}</p>
    </div>
</div>
</template>

<style scoped>
.performers-list-div {
    width: 424px;
    height: 110px;
    border-radius: 20px;
    background-color: #fff;
    border: 1px solid #000;
    overflow-y: auto;
    padding-left: 11px;

    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 5;

    scrollbar-width: thin;
    scrollbar-color: rgba(0,0,0,0) rgba(0,0,0,0);
}

.performers-list-div::-webkit-scrollbar {
    width: 3px; /* Толщина скроллбара */
    margin-right: 5px;
}

.performers-list-div::-webkit-scrollbar-track {
    background: rgba(0,0,0,0); /* Полностью прозрачная дорожка */
    margin: 5px 0; /* Отступ сверху и снизу */
    margin-right: 5px;
}

.performers-list-div::-webkit-scrollbar-thumb {
    background-color: #888; /* Серый цвет ползунка */
    border-radius: 3px; /* Закругленные углы */
    border: 1px solid transparent; /* Прозрачная граница */
    background-clip: content-box; /* Чтобы фон не заходил за границы */
    margin-right: 5px;
}

@supports (scrollbar-width: thin) {
    .performers-list-div {
        scrollbar-color: #888 rgba(0,0,0,0); /* Серый ползунок на прозрачном фоне */
        margin-right: 5px;
    }
}

.performers-div p {
    font-family: Cormorant;
    font-size: 24px;
    font-weight: 400;
    color: #000;
}
</style>
