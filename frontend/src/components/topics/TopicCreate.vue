<template>
  <v-container>
    <h1>Create Topic</h1>
    <v-alert v-if="error" type="error">{{ error }}</v-alert>
    <v-form ref="form" @submit.prevent="submitForm">
      <v-text-field v-model="topic.title" label="Title" required></v-text-field>
      <v-text-field v-model="topic.description" label="Description" required></v-text-field>
      <v-btn type="submit" color="primary">Save</v-btn>
      <v-btn color="error" class="mx-2" @click="cancel">Cancel</v-btn>
    </v-form>
  </v-container>
</template>
<script>
import apiClient from "../../lib/apiClient";
import { useAuth0 } from '@auth0/auth0-vue';


export default {
  name:"TopicCreate",
  data() {
    return {
      topic: {
        title: "",
        description: ""
      },
      error: null
    };
  },
  setup(){
    const { getAccessTokenSilently } = useAuth0();
        return {
            getAccessTokenSilently
        };
  },
  methods: {
    async submitForm() {
      if (this.$refs.form.validate()) {
        const token = await this.getAccessTokenSilently();
        try{
          await apiClient.createTopic(this.topic, token);
          this.$router.push({ name: "TopicList" });
        }catch(error){
          console.log(error)
          this.error = "The topic could not be created:"  + error;
        }
      }
    },
    cancel() {
        this.$router.push({ name: "TopicList" });
      },
  }      
};
</script>
