<script setup>
import { ref } from "vue";
import api from "../api.js";

// Components
import Splitter from "primevue/splitter";
import SplitterPanel from "primevue/splitterpanel";
import ScrollPanel from "primevue/scrollpanel";
import SubjectPanel from "../components/SubjectPanel.vue";
import VocabTree from "../components/VocabTree.vue";

// State
const currentSubject = ref(null);

// Event Handlers
async function onSubjectSelected(subject_info) {
    const detailUrl = subject_info._links.detail;
    currentSubject.value = await api.getData(detailUrl);
}
</script>
<template>
    <Splitter class="fixed top-[6px] bottom-0 left-0 right-0">
        <SplitterPanel :size="30" :minSize="25">
            <ScrollPanel
                class="w-full h-full"
                :dt="{ bar: { background: '#CCC' } }"
            >
                <VocabTree @subjectSelected="onSubjectSelected"></VocabTree>
            </ScrollPanel>
        </SplitterPanel>
        <SplitterPanel :size="60" :minSize="50">
            <ScrollPanel
                class="w-full h-full"
                :dt="{ bar: { background: '#CCC' } }"
            >
                <SubjectPanel v-if="currentSubject" :subject="currentSubject">
                </SubjectPanel>
            </ScrollPanel>
        </SplitterPanel>
    </Splitter>
</template>
