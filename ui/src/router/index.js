import { createWebHistory, createRouter } from "vue-router"
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import Map from '../views/Map.vue'
import Entries from '../views/Entries.vue'
import store from '../store'

const routes = [
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/",
    name: "Dashboard",
    component: Dashboard,
  },
  {
    path: "/entries",
    name: "Entries",
    component: Entries,
  },
  {
    path: "/entry/:id",
    name: "Entry",
    component: Entries,
  },
  {
    path: "/map",
    name: "Map",
    component: Map,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, from) => {
  console.log(from, to)
  if (to.path === '/login') return true
  if (!store.getters['user/isLoggedIn']) return '/login'
})

export default router;