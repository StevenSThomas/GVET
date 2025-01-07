<script>
import "primeicons/primeicons.css"
import Button from "primevue/button"
import Hello from "./components/hello.vue"
import {useStore} from "./store.js"
import { defineComponent } from "vue"

export default defineComponent({
    setup(){
        const store = useStore();
        store.fetchFacets();
        return {store};

    },
    components: {
        Button,
        Hello
    }
});
</script>

<template>
 <div>
    <section v-for="facet in store.facets"> 
        <div>{{ facet.label }}</div>
        <p style="padding:20px">{{ facet.note }}</p>
    </section>
 </div>
</template>
