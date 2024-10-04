import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/usuarios/LoginView.vue'
import PruebaView from '../views/prueba/PruebaView.vue'
import RegistroUsuarioView from '../views/usuarios/RegistroUsuarioView.vue'
import RegistroUsuarioConfirmacionView from '../views/usuarios/RegistroUsuarioConfirmacionView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginView
    },
    {
      path: '/prueba',
      name: 'prueba',
      component: PruebaView
    },
    {
      path: "/usuarios",
      children: [
        { path: 'registro', component: RegistroUsuarioView },
        { path: 'confirmar/:token', component: RegistroUsuarioConfirmacionView, props: true },
      ],
    },
  ]
})

export default router
