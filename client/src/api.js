/**
 *  API to the server
 */

/**
 * simple wrapper around fetch
 */
import { ref } from "vue";

export const isLoading = ref(false);

async function getData(endpoint) {
  const apiUrl = "http://127.0.0.1:5000/api";
  try {
    let endpointUrl = null;
    isLoading.value = true;
    if (endpoint.includes("http")) {
      endpointUrl = endpoint;
    } else {
      endpointUrl = `${apiUrl}${endpoint}`;
    }
    const response = await fetch(endpointUrl);
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    alert(error);
  } finally {
    isLoading.value = false;
  }
}

export default {
  getData,
  async getSubjectDetail(subject_id) {
    return await getData(`/subjects/${subject_id}`);
  },
  async getFacets() {
    return await getData("/facets");
  },
  async search(term) {
    return await getData(
      "/search/" + new URLSearchParams({ q: term }).toString(),
    );
  },
};
