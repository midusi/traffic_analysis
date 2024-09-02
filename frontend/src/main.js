import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Toaster from "@meforma/vue-toaster";

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(Toaster, {
    position: "top",
    duration: 6000,
});

app.mount('#app')
