import {createRouter, createWebHistory} from 'vue-router'  
import AdminPage from "./pages/AdminPage";
import HomePage from "./pages/HomePage";
import { authGuard } from "@auth0/auth0-vue";

import TopicList from "./components/topics/TopicList";
import TopicCreate from "./components/topics/TopicCreate.vue";
import TopicEdit from "./components/topics/TopicEdit.vue";
import ChatComponent from "./components/ChatComponent.vue";

const routes=[
  {
      path: '/',
      name: 'Home',
      component: HomePage
  },
  {
      path: '/admin',
      name: 'Topics',
      component: AdminPage,
      beforeEnter: authGuard,
  }, 
  {
    path: "/admin/topics",
    name: "TopicList",
    component: TopicList,
    beforeEnter: authGuard,
  },
  {
    path: "/admin/topics/create",
    name: "TopicCreate",
    component: TopicCreate,
    beforeEnter: authGuard,

  },
  {
    path: "/admin/topics/edit/:id",
    name: "TopicEdit",
    component: TopicEdit,
    beforeEnter: authGuard,
    props: true,
  },
  {
    path: "/admin/chat/:topicId",
    name: "ChatComponent",
    component: ChatComponent,
    beforeEnter: authGuard,

    props: true,
  },
]
const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router;