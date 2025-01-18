<script setup>
import { computed } from "vue";
import Panel from "primevue/panel";

// sub-components
//
import Breadcrumb from "primevue/breadcrumb";
import RecordTypeIcon from "./RecordTypeIcon.vue";
import TermsList from "./TermsList.vue";
import SectionTitle from "./SectionTitle.vue";

// properties
const props = defineProps(["subject", "loading"]);

// the preferred note is the the first note in the subject's note list
const preferredNoteText = computed(() => {
    if (
        props.subject &&
        props.subject.notes &&
        props.subject.notes.length > 0
    ) {
        return props.subject.notes[0].text;
    }
    return "";
});

const additionalNotes = computed(() => {
    if (
        props.subject &&
        props.subject.notes &&
        props.subject.notes.length > 1
    ) {
        return props.subject.notes.slice(1);
    }
    return false;
});
</script>
<style scoped>
.p-panel {
    border-radius: 0;
}
</style>
<template>
    <Panel v-if="subject">
        <template #header>
            <h2 class="text-xl font-bold">{{ subject.name }}</h2>
        </template>
        <template #icons>
            <div
                v-if="subject.record_type"
                class="flex items-center gap-1 text-lg font-semibold text-purple-600 mr-2"
            >
                <RecordTypeIcon :subject="subject"></RecordTypeIcon>
                <span>{{ subject.record_type }}</span>
            </div>
        </template>
        <div class="mt-2 flex flex-col gap-6">
            <div
                v-if="subject.ancestors"
                class="text-xs flex flex-wrap gap-2 text-slate-500"
            >
                <div
                    v-for="ancestor in subject.ancestors"
                    class="flex items-center gap-1 whitespace-nowrap"
                >
                    <div>|</div>
                    <RecordTypeIcon
                        style="font-size: 0.6rem"
                        :subject="ancestor"
                    >
                    </RecordTypeIcon>
                    {{ ancestor.name }}
                </div>
            </div>
            <section>
                <p class="max-w-[800px]">{{ preferredNoteText }}</p>
            </section>
            <section>
                <SectionTitle>Terms</SectionTitle>
                <TermsList :subject="subject"></TermsList>
            </section>
            <section v-if="additionalNotes">
                <SectionTitle>Additional Notes</SectionTitle>
                <div class="my-8" v-for="note in additionalNotes">
                    <div class="mb-1 text-sm font-bold text-slate-400">
                        {{ note.language.replace("(language)", "") }}:
                    </div>
                    <div class="max-w-[800px]">
                        {{ note.text }}
                    </div>
                </div>
            </section>
            <section v-if="subject.ancestors">
                <SectionTitle>Hierarchical Position</SectionTitle>
                <div>
                    <div class="p-2">
                        <div v-for="(ancestor, index) in subject.ancestors">
                            <span class="flex gap-2 items-baseline">
                                <span
                                    v-for="space in index"
                                    class="w-1 whitespace-normal text-slate-500 text-xs"
                                    >.</span
                                >
                                <RecordTypeIcon
                                    class="text-blue-700"
                                    style="font-size: 0.8rem"
                                    :subject="ancestor"
                                >
                                </RecordTypeIcon>
                                <span>{{ ancestor.name }}</span>
                            </span>
                        </div>
                    </div>
                </div>
            </section>
        </div>
        <footer class="flex justify-end gap-1">
            <div class="text-sm text-slate-400">
                {{ subject.id }}
            </div>
        </footer>
    </Panel>
</template>
