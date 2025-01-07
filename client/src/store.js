import { defineStore } from "pinia";
import api from "./gvp";

export const useStore = defineStore({
    id: "store",
    state: () => ({
        loading: false,
        facets: [],
        error: null
    }),
    actions: {
        async fetchFacets() {
            this.facets = [];
            this.loading = true;
            try {
                this.facets = await api.getFacets();
            } catch (error) {
                this.error = error;
            } finally {
                this.loading = false;
            }
        }
    }
})