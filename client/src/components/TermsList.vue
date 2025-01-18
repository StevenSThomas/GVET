<script setup>
import { computed } from "vue";
import { groupBy } from "../utils.js";

const props = defineProps(["subject"]);

// remove '(language)' from the language text
const normalizedTerms = computed(() => {
    if (props.subject && props.subject.terms.length > 0)
        return props.subject.terms.map((term) => {
            term.language = term.language.replace("(language)", "").trim();
            return term;
        });
    return [];
});

// group terms by language
const groupedTerms = computed(() => {
    return groupBy(normalizedTerms.value, "language");
});
</script>
<template>
    <div class="my-4" v-for="(terms, language) of groupedTerms">
        <div class="mb-2 text-xs text-slate-500 font-semibold">
            {{ language }}:
        </div>
        <div class="ml-4 mb-1 flex items-baseline gap-2" v-for="t in terms">
            <div :class="{
                '': t.type === 'preferred' || t.type === 'gvp_preferred',
                italic: t.type === 'alternative',
            }">
                {{ t.label }}
            </div>
            <div class="text-sm flex items-baseline text-slate-500 gap-4">
                <div v-if="t.type === 'alternative'">alternative</div>
                <div class="lowercase">{{ t.part_of_speech }}</div>
            </div>
        </div>
    </div>
</template>
