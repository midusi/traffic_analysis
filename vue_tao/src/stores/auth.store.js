import { defineStore } from 'pinia'
import { jwtDecode } from 'jwt-decode';

import router from '../router'
import { fetchWrapper } from '../helpers'

export const useAuthStore = defineStore({
  id: 'auth',
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')),
    returnUrl: null
  }),
  actions: {
    async login(email, password) {
      const user = await fetchWrapper.post(
        `https://admin-grupo14.proyecto2023.linti.unlp.edu.ar/api/auth/`,
        { email, password }
      )
      console.log(user)

      this.user = user
      localStorage.setItem('user', JSON.stringify(user))

      router.push(this.returnUrl || '/')
    },
    getUserId() {
      if (!localStorage.getItem('user')) return false;

      const user = jwtDecode(JSON.parse(localStorage.getItem('user')).token);
      console.log(user);
      return user?.id;
    },
    getUserRole() {
      if (!localStorage.getItem('user')) return false;

      const user = jwtDecode(JSON.parse(localStorage.getItem('user')).token);
      return user.es_admin;
    },
    logout() {
      this.user = null
      localStorage.removeItem('user')
      router.push('/login')
    },
    isLoggedIn() {
      return this.user
    }
  }
})
