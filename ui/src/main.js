import { createApp } from 'vue'
import App from './App.vue'
import naive from 'naive-ui'
import router from './router'
import store from './store';
import VueGoodTablePlugin from 'vue-good-table-next';
import 'vue-good-table-next/dist/vue-good-table-next.css'

console.log('Environment: ', import.meta.env.MODE)
console.log('ENV: ', import.meta.env)

createApp(App)
  .use(naive)
  .use(router)
  .use(store)
  .use(VueGoodTablePlugin)
  .mount('#app')
