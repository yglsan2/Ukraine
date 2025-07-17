import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import BooksView from '../views/BooksView.vue'
import EventsView from '../views/EventsView.vue'
import AssociationView from '../views/AssociationView.vue'
import ChatbotView from '../views/ChatbotView.vue'
import AboutView from '../views/AboutView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/books',
      name: 'books',
      component: BooksView
    },
    {
      path: '/events',
      name: 'events',
      component: EventsView
    },
    {
      path: '/association',
      name: 'association',
      component: AssociationView
    },
    {
      path: '/chatbot',
      name: 'chatbot',
      component: ChatbotView
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView
    }
  ]
})

export default router
