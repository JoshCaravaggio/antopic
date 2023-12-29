<!-- Podcast.vue -->
<template>
  <v-card class="podcast" outlined>
    <v-card-title>{{ podcast.title }}</v-card-title>
    <v-card-subtitle>Creator: {{ podcast.creator }}</v-card-subtitle>
    <v-card-text>Published: {{ formattedDate }}</v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'PodcastComponent',
  props: {
    podcast: {
      type: Object,
      required: true,
    },
  },
  computed: {
    formattedDate() {
      return new Date(this.podcast.publishedDate).toLocaleDateString();
    },
  },
};
</script>

<style scoped>
.podcast {
  margin-bottom: 1rem;
}
</style>
