<template>  
  <v-app id="app">
    <v-app-bar app absolute color="primary" :elevation="2">    
      <v-app-bar-title @click="goHome" >Antopic</v-app-bar-title>
      <v-btn class="mx-4 white--text" v-if="isAuthenticated" elevation="2" x-large rounded color="white" to="/admin">
            Topics
          </v-btn>
      <login-button v-if="!(isAuthenticated)" ></login-button>
      <logout-button  v-else @click="logout">Log out</logout-button>  
    </v-app-bar>
      <v-main>
        <router-view/>
    </v-main>
    <v-footer app color="primary" :elevation="2">
      <v-row class="d-flex justify-center">
        <v-col cols="12" md="6" class="text-center">
          <span class="white--text">Antopic 2023</span>
        </v-col>
      </v-row>
      </v-footer> 
    </v-app>
</template>
<script>

import { useTheme } from 'vuetify'
import { useAuth0 } from '@auth0/auth0-vue'; 
import LoginButton from './components/LoginButton.vue';
import LogoutButton from './components/LogoutButton.vue';

export default {

  name: "App",
  metaInfo: {
    title: 'Antopic',
    titleTemplate: '%s | Your Personalized Knowledge'
  },
  components: {
    LoginButton,
    LogoutButton,
  },
  setup(){
    const { isAuthenticated, user} = useAuth0();
    return {
      isAuthenticated,
      user
    }
  },
  methods:{
    setup(){
      const theme = useTheme()

    const { isAuthenticated, user} = useAuth0();
    return {
      theme,
      isAuthenticated,
      user
    }
    },
    goHome(){
      this.$router.push({name: "Home"});
    }
  }
};
</script>

<style>
</style>
