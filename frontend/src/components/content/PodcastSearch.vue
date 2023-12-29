<!-- PodcastSearch.vue -->
<template>
    <div>
      <v-app>
        <v-main>
          <v-container>
            <h1>Podcast Search</h1>
            <v-text-field
              v-model="searchQuery"
              label="Search for podcasts"
              @input="debouncedSearch"
              clearable
            ></v-text-field>
            <v-progress-linear
              v-if="loading"
              indeterminate
              class="mt-3"
            ></v-progress-linear>
            <div v-if="!loading && searchResults.length > 0">
              <Podcast
                v-for="(item, index) in searchResults"
                :key="index"
                :podcast="item"
              />
            </div>
          </v-container>
        </v-main>
      </v-app>
    </div>
  </template>
  <script>

  import Podcast from './PodcastComponent';
  import { debounce } from 'lodash';
  import podcastClient from '@/lib/podcastClient';
  
  export default {
    components: {
      Podcast,
    },
    data() {
      return {
        searchQuery: '',
        searchResults: [],
        loading: false,
      };
    },
    methods: {
      search() {
        if (this.searchQuery.trim()) {
          this.loading = true;
            podcastClient.search(this.searchQuery).then((results) => {
            this.searchResults = results;
            this.loading = false;
          });
        } else {
          this.searchResults = [];
        }
      },
    },
    mounted() {
      this.debouncedSearch = debounce(this.search, 300);
    },
  };
  </script>
  