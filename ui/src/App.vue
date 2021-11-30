<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
// import Map from './components/Map.vue'
import { ref, h, resolveComponent } from 'vue'
const title = ref(`${import.meta.env.VITE_APP_TITLE} ${import.meta.env.VITE_APP_VERSION}`)

const activeKey = ref(null)
function routeTo(target) {
  $router.push(target)
}
const menuOptions = [
  {
    label: () =>
        h(
          resolveComponent('router-link'),
          {
            to: '/',
          },
          {
            default: () => ['Dashboard']
          }
        ),
      key: 'menu-home',
      // icon: renderIcon(BookIcon)
  },
  {
    label: () =>
        h(
          resolveComponent('router-link'),
          {
            to: '/entries',
          },
          {
            default: () => ['Entries']
          }
        ),
      key: 'menu-entries',
      // icon: renderIcon(BookIcon)
  },
  {
    label: () =>
        h(
          resolveComponent('router-link'),
          {
            to: '/map',
          },
          {
            default: () => ['Map']
          }
        ),
      key: 'menu-map',
      // icon: renderIcon(BookIcon)
  }
]
</script>

<template>
  <h3>
  {{ title }}
  </h3>
  <n-menu v-model:value="activeKey" mode="horizontal" :options="menuOptions" />
  <hr />
  <router-view />
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 5px;
}
</style>
