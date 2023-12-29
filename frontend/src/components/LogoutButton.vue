<template>
      <v-btn class="mx-4 white--text"  elevation="2" x-large rounded color="white" @click="logout">Log out</v-btn>
  </template>
<script>
    import { useAuth0 } from '@auth0/auth0-vue';
  
    export default {
      setup() {
        const { logout } = useAuth0();

        return {
          logout: () => {
            logout({ logoutParams: { returnTo: window.location.origin } });
          }
          
        };
      }
    };
</script>