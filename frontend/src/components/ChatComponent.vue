<template>
  <v-main class="mx-auto flex flex-col">
    <div class="text-h3 font-bold leading-[1.1] tracking-tighter text-center">
      {{ this.topic.title }}
    </div>
    <div class="text-subtitle font-bold leading-[1.1] tracking-tighter text-center">
      {{ this.topic.description }}
    </div>
    
    <v-container>
      <v-row class="flex-grow-1">
        <v-col cols="12">
          <v-card
            ref="messageListRef"
            flat
            class="message-list overflow-y-auto d-flex flex-column"
          >
            <v-card-text>
              <div
                v-for="(message, index) in chatMessages"
                :key="`chatMessage-${index}`"
              >
                <v-row
                  :class="[
                    message.type === 'apiMessage'
                      ? 'api-message'
                      : 'user-message',
                    {
                      'user-message-waiting':
                        message.type === 'userMessage' &&
                        loading &&
                        index === chatMessages.length - 1,
                    },
                  ]"
                  align="center"
                >
                  <v-col cols="1">
                    <v-img
                      :src="message.type === 'apiMessage'
                        ? '/bot-image.png'
                        : '/usericon.png'"
                      :alt="message.type === 'apiMessage' ? '' : 'Me'"
                      width="40"
                      height="40"
                    />
                  </v-col>
                  <v-col>
                    <div class="markdown-answer">
                      <vue3-markdown>{{
                        message.message
                      }}</vue3-markdown>
                    </div>
                  </v-col>
                </v-row>
                <div
                  v-if="message.sourceDocs"
                  class="p-5"
                  :key="`sourceDocsAccordion-${index}`"
                >
                  <v-expansion-panels multiple>
                    <v-expansion-panel
                      v-for="(doc, index) in message.sourceDocs"
                      :key="`messageSourceDocs-${index}`"
                    >
                      <v-expansion-panel-header>
                        <h3>Source {{ index + 1 }}</h3>
                      </v-expansion-panel-header>
                      <v-expansion-panel-content>
                        <vue-markdown>{{
                          doc.pageContent
                        }}</vue-markdown>
                        <p class="mt-2">
                          <b>Source:</b> {{ doc.metadata.source }}
                        </p>
                      </v-expansion-panel-content>
                    </v-expansion-panel>
                  </v-expansion-panels>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <v-form @submit.prevent="handleSubmit">
            <v-textarea
            
              v-model="query"
              :disabled="loading"
              auto-grow
              rows="3"
              maxLength="512"
              id="userInput"
              name="userInput"
              :placeholder="this.placeholder"
              solo
              outlined
              class="textarea row"
            />
            <v-btn
              type="submit"
              :disabled="loading"
              class="generate-button"
              color="primary"
              block
            >
              <v-icon v-if="!loading">mdi-send</v-icon>
              <v-progress-circular v-else indeterminate color="white" />
            </v-btn>
          </v-form>
          <div v-if="error" class="border border-red-400 rounded-md p-4">
            <p class="text-red-500">{{ error
            }}</p>
          </div>
        </v-col>
      </v-row>
    </v-container>
    <v-footer class="m-auto p-4"></v-footer>
  </v-main>
</template>    
  <script>
  import Vue3Markdown from "vue3-markdown";
  import apiClient from "../lib/apiClient";
  import { useAuth0 } from '@auth0/auth0-vue';
  
export
  default {
  components: {
    Vue3Markdown,
  },
  props:["topicId"],
  data() {
    return {
      query: "",
      loading: false,
      placeholder: null,
      sourceDocs: [],
      error: null,
      messageState: {
        messages: [
        ],
        history: [],
        pendingSourceDocs: [],
      },
      topic:null
    };
  },
  computed: {
    messages() {
      return this.messageState.messages;
    },
    pending() {
      return this.messageState.pending;
    },
    history() {
      return this.messageState.history;
    },
    pendingSourceDocs() {
      return this.messageState.pendingSourceDocs;
    },
    chatMessages() {
      return [
        ...this.messages,
        ...(this.pending
          ? [
              {
                type: "apiMessage",
                message: this.pending,
                sourceDocs: this.pendingSourceDocs,
              },
            ]
          : []),
      ];
    },
  },
  mounted() {
    this.fetchHistory();
  },
  setup() {
    const { getAccessTokenSilently } = useAuth0();
    return {
      getAccessTokenSilently,
    };
  },
  async created(){
    this.topic = await apiClient.getTopic(this.topicId, await this.getAccessTokenSilently());
    apiClient.getTopicPlaceholder(this.topicId, await this.getAccessTokenSilently()).then((data) => {
      this.placeholder = data;
    });

  },
  methods: {
    async handleSubmit() {
      this.placeholder =  null;
      if (!this.query) {
        this.error = "Please input a question";
        return;
      }
      const question = this.query.trim();
      this.messageState.messages.push({
        type: "userMessage",
        message: question,
      });
      this.loading = true;
      this.query = "";
      this.messageState.pending = "";

      try {
        const response = await apiClient.chat(
            this.topicId, 
            question, 
            history, 
            await this.getAccessTokenSilently())
        this.updateMessages(response);            
      } 
      catch (error) {
        this.loading = false;
        this.error = "An error occurred while fetching the data. Please try again.";
        console.log("error", error);
      }
    },
    async fetchHistory() {
        // try {
        //     const response = await fetch(`/api/history/${this.topicId}`);
        //     const data = await response.json();
        //     this.messageState.messages = data.messages;
        //     this.messageState.history = data.history;
        // } catch (error) {
        //     this.error = "An error occurred while fetching the chat history. Please try again.";
        //     console.log("error", error);
        // }
    },
    updateMessages(update) {
        console.log(update)
        this.messageState.history.push([update, this.messageState.pending||""]);
        this.messageState.messages.push({
            type: "apiMessage",
            message: update.answer||"",
            sourceDocs: this.messageState.pendingSourceDocs,
        });
        this.messageState.pending=undefined;
        this.messageState.pendingSourceDocs=undefined;
        this.loading=false;
    }
  },
};
</script>

<style scoped>
/* Add your custom styles here */
</style>

function newFunction(question) {
  this.messageState.history.push([question, this.messageState.pending||""]);
  this.messageState.messages.push({
    type: "apiMessage",
    message: this.messageState.pending||"",
    sourceDocs: this.messageState.pendingSourceDocs,
  });
  this.messageState.pending=undefined;
  this.messageState.pendingSourceDocs=undefined;
  this.loading=false;
}
  