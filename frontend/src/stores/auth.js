import { defineStore } from 'pinia'
import { apiService } from '@/services/api';
import axios from 'axios';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null,
        isAuthenticated: false,
        loading: false,
        error: null,
    }),
    actions: {
        async loginUser(credentials) {
            this.loading = true
            this.error = null
            try {
                const response = await axios.post(import.meta.env.VITE_API_URL + "auth", {
                    withCredentials: true, // Importante para enviar cookies
                })

                if (response.status !== 200) {
                    throw new Error('Login failed')
                }

                // Obtener la información del usuario
                await this.fetchUser()
            } catch (error) {
                this.error = error.response ? error.response.data.message : error.message
            } finally {
                this.loading = false
            }
        },
        async logoutUser() {
            this.loading = true
            this.error = null
            try {
                const response = await apiService.post('logout', {})

                if (response.status !== 200) {
                    throw new Error('Logout failed')
                }

                // Limpiar el estado
                this.user = null
                this.isAuthenticated = false
            } catch (error) {
                this.error = error.response ? error.response.data.message : error.message
            } finally {
                this.loading = false
            }
        },
        async fetchUser() {
            try {
                const response = await apiService.get('me')

                if (response.status === 200) {
                    this.user = response.data
                    this.isAuthenticated = true
                } else {
                    throw new Error('Failed to fetch user')
                }
            } catch (error) {
                this.user = null
                this.isAuthenticated = false
                this.error = error.response ? error.response.data.message : error.message
            }
        },
    },
})
