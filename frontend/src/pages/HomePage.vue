<template>
  <v-app>
    <v-main>
      <v-container>
        <v-row class="mt-5">
          <v-col cols="12" class="text-center">
            <h1>Welcome to Antopic</h1>
            <h2>Your Personalized Knowledge Companion</h2>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12" md="6" lg="4">
            <v-card>
              <v-card-title>Curate Your Knowledge Universe</v-card-title>
              <v-card-text>Create and customize topics by adding a variety of content such as YouTube videos, podcasts, and PDFs.</v-card-text>
            </v-card>
            <!-- Prompt: Create a vector graphic representing the curation of different types of media, such as a YouTube video, podcast, and PDF, into a single topic. -->
          </v-col>

          <v-col cols="12" md="6" lg="4">
            <v-card>
              <v-card-title>Smart Contextual Processing</v-card-title>
              <v-card-text>Our AI chatbot processes the content within each topic, ensuring it understands the context and provides relevant, citable answers.</v-card-text>
            </v-card>
            <!-- Prompt: Create a vector graphic representing an AI chatbot processing and understanding context from different types of media, such as a YouTube video, podcast, and PDF. -->
          </v-col>

          <v-col cols="12" md="6" lg="4">
            <v-card>
              <v-card-title>Interactive Learning</v-card-title>
              <v-card-text>Chat with your topics to gain insights, ask questions, and have discussions with our AI-powered chatbot.</v-card-text>
            </v-card>
            <!-- Prompt: Create a vector graphic representing a person having an interactive conversation with an AI chatbot about a specific topic, with chat bubbles representing their discussion. -->
          </v-col>

          <v-col cols="12" md="6" lg="4">
            <v-card>
              <v-card-title>Easy Collaboration</v-card-title>
              <v-card-text>Share your curated topics with friends, classmates, or colleagues, and learn together through interactive discussions.</v-card-text>
            </v-card>
            <!-- Prompt: Create a vector graphic representing a group of people collaborating on a shared topic, with various types of media like a YouTube video, podcast, and PDF, and chat bubbles to indicate discussion. -->
          </v-col>

          <v-col cols="12" md="6" lg="4">
            <v-card>
              <v-card-title>Stay Organized</v-card-title>
              <v-card-text>Manage and access all your topics in one convenient location, making it easier to explore, learn, and track your progress.</v-card-text>
            </v-card>
            <!-- Prompt: Create a vector graphic representing an organized digital space with different topics and media types, such as a YouTube video, podcast, and PDF, neatly arranged and easily accessible. -->
          </v-col>
          </v-row>
          <v-row class="mt-5">
          <v-col cols="12" class="text-center">
            <v-btn color="primary" @click="loginWithRedirect" large>Sign Up Now</v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-main>

    <!-- Add your app's footer, if desired -->
  </v-app>
</template>

  <script>
      import { useAuth0 } from '@auth0/auth0-vue'; 
    export default {
        name: "HomePage",
        setup() {
            const { loginWithRedirect } = useAuth0();
            return {
                loginWithRedirect
            };
        },
    //     setup() {
    //     const { isAuthenticated,  } = useAuth0();
    //     console.log(isAuthenticated)
    //     if(isAuthenticated)
    //     {
    //         window.location.href = "/admin/topics";
    //     }
    // }
    };
  </script>