<template>
    <v-container fluid>        
            <topic-list />
    </v-container>
  </template>
  <script>

    import { useAuth0 } from '@auth0/auth0-vue'; 
    import TopicList from "./../components/topics/TopicList.vue"

    export default {
    name: "AdminPage",
    components:{
        TopicList,  
    },
    data () {       
        return{
        }
    },
    setup() {
        const { user, isAuthenticated, getAccessTokenSilently } = useAuth0();
        return {
            user,
            isAuthenticated, 
            getAccessTokenSilently
        };
    },
    async created () {
    },
    methods:{

    } 
};
  </script>