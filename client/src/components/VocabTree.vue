<script setup>
import { ref, watch } from "vue";
import { useRoute } from "vue-router";
import api from "../api.js";
import Tree from "primevue/tree";

const emit = defineEmits(["subjectSelected"]);
const nodes = ref([]);
const selectedKey = ref(null);

initTree();

// initializes the tree with the root elements (Facets)
async function initTree() {
    const facets = await api.getFacets();
    nodes.value = buildNodes(facets);
}

// builds tree nodes from subject objects from server.
function buildNodes(subject_list) {
    return subject_list.map((subject) => {
        return {
            key: subject.id,
            label: subject.name,
            data: subject,
            leaf: false,
        };
    });
}

async function onNodeExpand(node) {
    if (!node.children) {
        node.children = await getNodeDescendants(node);
    }
}

async function onNodeSelect(node) {
    emit("subjectSelected", node.data);
}

async function getNodeDescendants(node) {
    node.loading = true;
    const descendantUrl = node.data._links.preferred_descendants;
    const response = await api.getData(descendantUrl);
    node.loading = false;
    return buildNodes(response);
}
</script>
<style>
.p-tree-node-content {
    --p-tree-node-padding: 0 0 0 0;
    padding: 0 0 0 0;
}
</style>
<template>
    <div class="text-sm">
        <Tree
            loadingMode="icon"
            :value="nodes"
            @node-expand="onNodeExpand"
            @node-select="onNodeSelect"
            v-model:selectionKeys="selectedKey"
            selectionMode="single"
        >
        </Tree>
    </div>
</template>
