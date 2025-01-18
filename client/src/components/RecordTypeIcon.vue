<script setup>
import { computed } from "vue";
const props = defineProps(["subject"]);
const typeIcon = computed(() => {
    const icons = {
        Concept: "pi-lightbulb",
        Hierarchy: "pi-sitemap",
        Facet: "pi-box",
        GuideTerm: "pi-map",
    };
    if (props.subject) return icons[props.subject.record_type];
});
</script>
<template>
    <i class="pi" :class="typeIcon"></i>
</template>
