import { createApp } from 'vue'
import router from './routes'
import App from './App.vue'
import { createAuth0 } from '@auth0/auth0-vue';
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import "@mdi/font/css/materialdesignicons.css";

const app = createApp(App);

const myCustomLightTheme = {
  dark: false,
  colors: {
    background: '#FFFFFF',
    surface: '#FFFFFF',
    primary: '#6200EE',
    'primary-darken-1': '#3700B3',
    secondary: '#03DAC6',
    'secondary-darken-1': '#018786',
    error: '#B00020',
    info: '#2196F3',
    success: '#4CAF50',
    warning: '#FB8C00',
  }
}

app.config.productionTip = false;
app.use(router);

const vuetify = createVuetify({
    components,
    directives,
    icons: {    
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
    theme: {
      myCustomLightTheme    }
  },
})

app.use(
  createAuth0({
    domain: process.env.VUE_APP_AUTH0_DOMAIN,
    clientId: process.env.VUE_APP_AUTH0_CLIENT_ID,
    cacheLocation: 'localstorage',
    authorizationParams: {
      redirect_uri: window.location.origin,
      audience: process.env.VUE_APP_AUTH0_AUDIENCE,
      scope: 'email profile read:topics'
    }}),
);

app.use(vuetify)
app.mount('#app')
