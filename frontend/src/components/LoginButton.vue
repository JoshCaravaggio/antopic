<template>
    <v-btn class="mx-4"  elevation="2" x-large rounded color="white" variant="text" @click="login">
      Log in or Sign up
    </v-btn>
</template>
<script>
import { useAuth0 } from "@auth0/auth0-vue";

export default {
  name: "LoginButton",
  setup() {
    const { loginWithRedirect, user, isAuthenticated } = useAuth0();
    return {
      login() {
        loginWithRedirect();
      },
      user, 
      isAuthenticated
    };
  },
};
</script>

