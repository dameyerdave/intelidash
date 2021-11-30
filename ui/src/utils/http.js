import axios from 'axios'
import store from '../store';

const instance = axios.create({
  baseURL: import.meta.env.VITE_APP_BACKEND,
  timeout: 1000,
  headers: {
    'Content-Type': 'application/json'
  }
});

instance.interceptors.request.use((config) => {
  config.headers.Authorization = `JWT ${store.state.user.jwt}`
  return config;
})

export default instance