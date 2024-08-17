import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import 'tailwindcss/tailwind.css'
import './assets/style.css'

const urlDev = 'http://127.0.0.1:5000/'
const urlProd = 'https://admin-grupo14.proyecto2023.linti.unlp.edu.ar/'
const urlGlobal = urlProd

const app = createApp(App)

app.use(createPinia())
app.use(router)
//Vue.use(FlashMessage);
app.config.globalProperties.$urlGlobal = urlGlobal

app.mount('#app')
