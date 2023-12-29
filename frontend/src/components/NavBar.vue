<template>
  <v-layout>
    <v-navigation-drawer
    permanent
    location="left"
    theme="dark"
    >
    <template v-slot:prepend>
        <v-list-item
        lines="two"
        :title=user.name
        subtitle="Logged in"
        ></v-list-item>
    </template>            
    <v-divider>
      
    </v-divider>            
    <v-list density="compact" nav>        
        <v-list-item prepend-icon="mdi-home-city" title="Topics" value="home"></v-list-item>
        <v-list-item prepend-icon="mdi-account" title="Logout" value="account"></v-list-item>
    </v-list>
    </v-navigation-drawer>
    <v-main style="height: 250px"></v-main>
  </v-layout>
</template>
<script>
export default {
  name: "NavBar",
  props:{
    title: String,
    user:{
        given_name: String        
    }
  }
};
</script>

