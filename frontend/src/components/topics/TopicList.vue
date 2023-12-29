<!-- eslint-disable vue/valid-v-slot -->
<template>
  <v-container>
    <h1>Your Topics</h1>
    <v-row>
      <v-alert v-if="error" type="error">{{ error }}</v-alert>
      <v-col v-else cols="12" sm="6" md="6" lg="6" v-for="topic in topics" :key="topic._id">
  <v-progress-circular indeterminate color="primary" v-if="isLoading" />
  <v-card class="pa-3 mb-4">
    <v-row>
      <v-col cols="12" class="">
        <v-card-title>
          {{ topic.title }}
        </v-card-title>
      </v-col>
      <v-col cols="12">
        <v-chip v-if="topic.state === 'processing'" variant="outlined">
          Processing
        </v-chip>
      </v-col>
    </v-row>
    <v-card-actions>
      <v-btn small color="primary" @click="chat(topic._id)">Chat</v-btn>
      <v-btn small color="primary" class="outlines" @click="editTopic(topic._id)">Manage</v-btn>
    </v-card-actions>
  </v-card>
</v-col>

      <v-col cols="12">
        <v-btn color="primary" @click="createTopic">Create</v-btn>
      </v-col>
    </v-row>
  </v-container>

</template>
  <script>
  import   apiClient from "../../lib/apiClient";
  import { useAuth0 } from '@auth0/auth0-vue';

  export default {
    name:"TopicList",
    data() {
      return {
        headers: [
          { text: "ID", value: "_id" },
          { text: "Title", value: "title" }
        ],
        topics: [],
        isLoading:true,
        error: null

      };
    },
    setup() {
        const { getAccessTokenSilently } = useAuth0();
        return {
            getAccessTokenSilently
        };
    },
    async created() {
      try{
          const resp = await apiClient.getTopics(await this.getAccessTokenSilently());
          this.isLoading=false;
          this.topics = resp;
        }catch(error){
            this.isLoading=false;
            console.log("Error")
            console.log(error);
            this.error = error;
          }
    },
    methods: {
      createTopic() {
        this.$router.push({ name: "TopicCreate" });
      },
      editTopic(id) {
        console.log(id)
        this.$router.push({ name: "TopicEdit", params: { id } });
      },
      chat(id) {
        console.log(id)
        this.$router.push({ name: "ChatComponent", params: { topicId: id } });
      },
      async deleteTopic(id) {
        await apiClient.deleteReview(id, await this.getAccessTokenSilently());
        this.topics = this.topics.filter((review) => review.id !== id);
      },
    },
  };
  </script>
  