<template>
    <div class="textarea-container">
        <pre
            v-if="!isEditing"
            :id="id + '-highlight'"
            class="syntax-highlighted"
            v-html="highlightedCode"
            @click="toggleEdit"
        ></pre>

        <textarea
            v-else
            :id="id"
            :name="name"
            :placeholder="placeholder"
            v-model="inputCode"
            @blur="toggleEdit"
            :rows="rows"
        ></textarea>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import {inputCode} from '@/main.js'

const props = defineProps({
    id: String,
    name: String,
    rows: {
        type: Number,
        default: 150,
    },
    placeholder: String,
});
const isEditing = ref(false);

const color=(code) =>{
    const kw=/\b(subprogram|pentru|daca|atunci|altfel|executa|cat_timp|returneaza|sf_daca|sf_subprogram|adevarat|fals|scrie|repeta|pana_cand|sf_pentru|sf_cat_timp|citeste|div|mod)\b/g
    const op=/(\+|\-|\*|div|mod|\/|<--|<|>|=|\(|\)|,)/g
    const d=/([0-9]+(\.[0-9]+)?)/g
    code=code.replaceAll(op, (match) => `<span style="color: red">${match}</span>`)
    code=code.replaceAll(kw, (match) => `<span style="color: blue">${match}</span>`)
    code=code.replaceAll(d, (match) => `<span style="color: #ff00ff">${match}</span>`);
    return code;
}
const highlightedCode = computed(() => color(inputCode.value));

const toggleEdit = () => {
    isEditing.value = !isEditing.value;
};
</script>

<style scoped>
.textarea-container {
    position: relative;
    width: 100%;
    font-family: monospace;
    line-height: 1.5;
}

.syntax-highlighted {
    position: relative;
    width: 100%;
    padding: 10px;
    white-space: pre-wrap;
    word-wrap: break-word;
    font-family: monospace;
    line-height: 1.5;
    border: 1px solid #ccc;
    background: white;
    cursor: text;
}

textarea {
    width: 100%;
    padding: 10px;
    white-space: pre-wrap;
    word-wrap: break-word;
    font-family: monospace;
    line-height: 1.5;
    border: 1px solid #ccc;
    resize: none;
    overflow: auto;
}
</style>
