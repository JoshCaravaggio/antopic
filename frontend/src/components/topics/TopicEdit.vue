<template>
  <v-container>
    <v-row>
  <v-col cols="12">
    <v-alert v-if="error" @click="this.error = null" type="error">{{ error }}</v-alert>
    <v-form ref="form" @submit.prevent="submitForm">
      <v-text-field v-model="topic.title" label="Title" required></v-text-field>
      <v-text-field v-model="topic.description" label="Description" required></v-text-field>
    </v-form>
    <v-row class="d-flex justify-end">
      <v-btn
        color="error"
        class="mx-2"
        @click="confirmDelete = true"
      >
        Delete
      </v-btn>
      <v-btn
        color="primary"
        :loading="saving"
        @click="submitForm"
      >
        <v-icon>mdi-content-save</v-icon>
        Save
      </v-btn>
    </v-row>
    <v-dialog v-model="confirmDelete" max-width="400px">
      <v-card>
        <v-card-title>Delete Topic</v-card-title>
        <v-card-text>Are you sure you want to delete this topic?</v-card-text>
        <v-card-text>You will lose access to all content without a refund to tokens</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="confirmDelete = false">Cancel</v-btn>
          <v-btn color="red darken-1" text @click="deleteTopic">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="confirmDeleteContent" max-width="400px">
      <v-card>
        <v-card-title>Delete Content</v-card-title>
        <v-card-text>Are you sure you want to delete this content?</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="confirmDelete = false">Cancel</v-btn>
          <v-btn color="red darken-1" text @click="deleteContent">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-col>
</v-row>

    <v-row class="d-flex ">
      <v-col cols="12">
        <h2 class="mx-2">Content</h2>
        <p class="mx-2">Add any content you'd like your topic ChatBot to be able to reference</p>
      </v-col>
</v-row>

<v-row>
  <v-col cols="12" v-for="content in contents" :key="content._id">
    <v-card class="pa-3 mb-4">
      <v-row class="d-flex align-center flex-wrap">
        <v-col cols="12" lg="10" class="">
          <v-card-title>
            <v-icon left>mdi-file-document-outline</v-icon>{{ content.title }}
          </v-card-title>
        </v-col>
        </v-row>
      <v-card-actions class="d-flex text-right">
        <v-chip v-if="content.state" color="primary" text-color="white">{{ content.state }}</v-chip>
        <!-- <v-btn small color="red darken-1"  @click=>Delete</v-btn> -->
        <v-btn
        color="error"
        class="mx-2"
        @click=" this.contentToDelete=content;confirmDeleteContent=true"
      >
        Delete
      </v-btn>
        <!-- this.contentToDelete=content;confirmDeleteContent=true" -->
      </v-card-actions>
    </v-card>
  </v-col>
  <v-dialog v-model="showAddContentModal" max-width="600px">
    <content-create @contentCreated="contentCreated" :topicId="this.topic._id" @close="showAddContentModal = false" @created="fetchContents"></content-create>
  </v-dialog>
  <v-dialog v-model="showAddContentModal" max-width="600px">
    <content-create @contentCreated="contentCreated" :topicId="this.topic._id" @close="showAddContentModal = false" @created="fetchContents"></content-create>
  </v-dialog>
</v-row>



    <v-row class="d-flex justify-end">

      <div>

        <v-btn         
        fixed
        fab
        top
        right
        color="primary" 
        class=" mx-2 "
        @click="showAddContentModal = true">
        Add </v-btn>        
      </div>
</v-row>
  </v-container>
</template>

<script>
import apiClient from "../../lib/apiClient";
import { useAuth0 } from "@auth0/auth0-vue";
import ContentCreate from "../content/ContentCreate.vue";

export default {
  name: "TopicEdit",
  components: {
    ContentCreate,
  },
  props: ["id"],
  data() {
    return {
      topic: {},
      contents: [],
      error: null,
      headers: [
        { text: "Filename", value: "filename" },
        { text: "Type", value: "type" },
        { text: "Actions", value: "actions", sortable: false },
      ],
      showAddContentModal: false,
      saving: false,
      confirmDelete: false,
      confirmDeleteContent: false,
      contentToDelete:null,
    };
  },
  setup() {
    const { getAccessTokenSilently } = useAuth0();
    return {
      getAccessTokenSilently,
    };
  },
  async created() {
    this.topic = await apiClient.getTopic(this.id, await this.getAccessTokenSilently());
    this.contents = this.topic.contents;
  },
  methods: {
    async fetchContents() {
    },
    async contentCreated( content) {
      console.log(content)
      this.contents.push(content);
      this.$forceUpdate();
    },
    async submitForm() {
      if (this.$refs.form.validate()) {
        const token = await this.getAccessTokenSilently();
        try{
          console.log(this.topic)
          await apiClient.updateTopic(this.topic._id,this.topic, token);
          this.$router.push({ name: "TopicEdit", params: { id: this.topic._id } });
        }catch(error){
          console.log(error)
          this.error = "The topic could not be update:"  + error;
        }
      }    
      },
    cancel() {
      // ...
    },
    async deleteTopic() {
      try {
        await apiClient.deleteTopic(this.topic._id, await this.getAccessTokenSilently());
        this.$router.push({ name: "TopicList" });
      } catch (error) {
        this.error = "The topic could not be deleted:" + error;
      }
    },
    async deleteContent() {
      try {
          await apiClient.deleteContent(this.contentToDelete._id, await this.getAccessTokenSilently());
          this.contents.splice(this.contents.findIndex(c => c._id == this.contentToDelete._id ), 1);
          this.contentToDelete = null;
          this.confirmDeleteContent = false;
      } catch (error) {
        this.error = "Content could not be deleted:" + error;
      }
    },
  },
};
</script>
          <v-btn small color="error" @click="this.contentToDelete=content;confirmDeleteContent=true">Delete</v-btn>
