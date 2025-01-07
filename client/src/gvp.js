const apiUrl = "http://127.0.0.1:5000/api";

export default {
    async getFacets() {
        return await fetch(apiUrl + "/facets").then((response) => response.json());
    }
}