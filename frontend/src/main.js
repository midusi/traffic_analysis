import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Toaster from "@meforma/vue-toaster";
import piniaPluginPersistedState from "pinia-plugin-persistedstate"

import App from './App.vue'
import router from './router'

const app = createApp(App)

const pinia = createPinia()
pinia.use(piniaPluginPersistedState)
app.use(pinia)
app.use(router)
app.use(Toaster, {
    position: "top",
    duration: 6000,
});

app.mount('#app')
