import HomeView from '../views/HomeView.vue';
import SearchView from '../views/SearchView.vue';
import ServiceView from '../views/ServiceView.vue';
import NotFoundView from '../views/NotFoundView.vue';
import RequestsView from '../views/RequestsView.vue';
import RequestView from '../views/RequestView.vue';
import ShowRequestView from '../views/ShowRequestView.vue';
import { createRouter, createWebHistory } from 'vue-router'
import LoginView from "../views/LoginView.vue";
import ProfileView from "../views/ProfileView.vue";
import StatsView from '../views/StatsView.vue';
import { useAuthStore } from '../stores/auth.store';


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/search',
      name: 'search',
      component: SearchView
    },
    {
      path: '/service/:id',
      name: 'service',
      component: ServiceView
    },
    {
      path: '/requests',
      name: 'requests',
      component: RequestsView
    },
    {
      path: '/request/:id',
      name: 'request',
      component: RequestView
    },
    {
      path: '/requests/:id',
      name: 'show-request',
      component: ShowRequestView,
      props: true
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/yo',
      name: 'profile',
      component: ProfileView
    },
    {
      path: '/stats',
      name: 'stats',
      component: StatsView
    },
    {
      path: "/:catchAll(.*)",
      name: 'not-found',
      component: NotFoundView
    }
  ]
})

router.beforeEach(async (to) => {
  const privatePages = ['/request'];
  // need to check for /service/:id but not literally :id, it can be 1, 2, etc
  const authRequired = privatePages.some(page => to.path.startsWith(page));

  const auth = useAuthStore();

  if (authRequired && !auth.user) {
    auth.returnUrl = to.fullPath
    return '/login'
  }
})

export default router
