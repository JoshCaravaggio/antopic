<template>
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="text-h5">Add Content</span>
        </v-card-title>
        <v-card-text>
          <v-alert v-if="error" type="error">{{ error }}</v-alert>
          <v-form ref="form" @submit.prevent="submitForm">
            <v-select
              :items="typesOptions"
              v-model="content.type"
              label="Content Type"
              selected="youtube"
            />  
            <input type="hidden" name="topic" v-model="content.topic" />
            <div v-if="content.type === 'youtube'">
              <v-text-field
                v-model="content.url"
                label="Youtube Link"
                @input="fetchYoutubeEmbed"
              />
              <p v-if="isValidVideo" class="text-success">{{youtubeValidationMsg}}</p>
              <p v-else-if="content.url" class="text-danger">Invalid video. {{this.youtubeValidationMsg}}</p>            
            </div>
            <div v-else>
              <v-file-input
                show-size
                accept=".mp3,.pdf,.txt"
                v-model="content.file"
                label="File input"
                @change="onFileChange"
              ></v-file-input>
              <v-text-field
                v-model="content.filename"
                label="Filename"
                readonly
              ></v-text-field>
            </div>
            <v-text-field
                v-model="content.title"
                label="Title"
              />
          </v-form>
        </v-card-text>
        <v-card-text >
            The content will begin uploading when you click save.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
          <v-btn color="blue darken-1" :loading="saving" text @click="submitForm">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </template>
  
  <script>
  import apiClient from "../../lib/apiClient";
  import { useAuth0 } from "@auth0/auth0-vue";
  
  export default {
    name: "ContentCreate",
    props: ["topicId"],
    data() {
        console.log("Topic ID Prop: " + this.topicId)
      return {
        dialog: true,
        content: {
          url: "",
          filename: "",
          file: null,
          type: "youtube",
          topic:this.topicId,
          title: ""
        },
        typesOptions: [
          { title: "Youtube URL", value: "youtube" },
          { title: "MP3 file", value: "mp3" },
          { title: "PDF", value: "pdf" },
          { title: "Text File", value: "txt" },
        ],
        saving:false,
        error: null,
        isValidVideo: false,
        youtubeValidationMsg:""
      };
    },
    setup() {
      const { getAccessTokenSilently } = useAuth0();
      return {
        getAccessTokenSilently,
      };
    },
    methods: {
      close() {
        this.$emit("close");
      },
      async submitForm() {
        this.saving = true;

        console.log("Attempting to create content");
        console.log(this.content);
        console.log("Topic: " + this.topicId);
        if (this.$refs.form.validate()) {
          try {
            const response = await apiClient.createContent(
              {
                ...this.content,
                file:
                  this.content.type === "youtube"
                    ? null
                    : this.content.file[0],
              },
              await this.getAccessTokenSilently()
            );
            this.$emit("content-created", response);
            this.close();
          } catch (error) {
            this.error = error;
            this.saving = false;
          }
        }
        this.saving = false;
      },

      extractVideoId(url) {
          const regex = /^.*(youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
          const match = url.match(regex);
        return match && match[2].length === 11 ? match[2] : null;
        },
      async fetchYoutubeEmbed() {
        const apiKey = "AIzaSyDh_8P8M2KBTyYpjfwd2Lf815iR4ofMULM";
        const videoId = this.extractVideoId(this.content.url);

        if (videoId) {
            try {
            const response = await fetch(
                `https://www.googleapis.com/youtube/v3/videos?id=${videoId}&part=snippet,contentDetails&key=${apiKey}`
            );
            const data = await response.json();
            if (data.items.length > 0) {
                const video = data.items[0];
                const isPublic = video.snippet.liveBroadcastContent === 'none';

                const duration = video.contentDetails.duration;
                //const videoTitle = video.contentDetails.title;
                const durationInSeconds = this.iso8601DurationToSeconds(duration);
                const isUnderOneHour = durationInSeconds <= 3600;

                if(!isPublic)
                    this.youtubeValidationMsg = "Video is not public";
                else if(!isUnderOneHour)
                    this.youtubeValidationMsg = "Video is longer than 1 hour";

                this.isValidVideo = isPublic && isUnderOneHour;

                if(this.isValidVideo)
                    this.youtubeValidationMsg = "Valid YouTube video";
                    this.content.title = video.snippet.localized.title;
                console.log(video)

            } else {
                this.isValidVideo = false;
            }
            } catch (error) {
            console.error("Error fetching YouTube video data:", error);
            }
        } else {
            this.isValidVideo = false;
        }
        },
        iso8601DurationToSeconds(duration) {
            const regex = /P(?:(\d+)D)?T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d{1,3})?)S)?/;
            const matches = duration.match(regex);

            const days = parseInt(matches[1], 10) || 0;
            const hours = parseInt(matches[2], 10) || 0;
            const minutes = parseInt(matches[3], 10) || 0;
            const seconds = parseFloat(matches[4]) || 0;

            return days * 86400 + hours * 3600 + minutes * 60 + seconds;
        },
      onFileChange() {
        console.log("Filename:" + this.content.file[0].name)
        this.content.filename = this.content.file[0].name;
        this.content.title = this.content.filename;
      },
    },
  };
  </script>
  