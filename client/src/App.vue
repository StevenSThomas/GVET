<script setup>
import { isLoading } from "./api.js";
import { computed } from "vue";

import "primeicons/primeicons.css";
import ProgressBar from "primevue/progressbar";
import Explorer from "./views/Explorer.vue";

const progressBarMode = computed(() => {
    if (isLoading.value) return "indeterminate";
    return null;
});
</script>
<template>
    <ProgressBar :mode="progressBarMode" style="height: 6px"></ProgressBar>
    <Explorer />
</template>
