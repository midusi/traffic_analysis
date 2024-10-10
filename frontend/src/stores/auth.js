import { defineStore } from 'pinia'
import { apiService } from '@/services/api';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null,
        isAuthenticated: false,
        loading: false,
        errors: null,
  }),
    persist: true,
    actions: {
        async loginUser(email, password) {
            this.loading = true
            this.errors = null
            try {
                const response = await apiService.post("auth/", {
                    "email": email,
                    "password": password
                })
                if (response.status !== 200) {
                    throw new Error('Login failed')
                }

                await this.fetchUser()
            } catch (error) {
                this.errors = error.response ? error.response.data.error : error.message
            } finally {
                this.loading = false
            }
        },
        async logoutUser() {
            this.loading = true
            this.errors = null
            try {
                const response = await apiService.get('auth/logout')

                if (response.status !== 200) {
                    throw new Error('Logout failed')
                }

                this.user = null
                this.isAuthenticated = false
            } catch (error) {
                this.errors = error.response ? error.response.data.error : error.message
            } finally {
                this.loading = false
            }
        },
        async fetchUser() {
            try {
                const response = await apiService.get('auth/me')

                if (response.status === 200) {
                    this.user = response.data
                    this.isAuthenticated = true
                } else {
                    throw new Error('Failed to fetch user')
                }
            } catch (error) {
                this.user = null
                this.isAuthenticated = false
                this.errors = error.response ? error.response.data.error : error.message
            }
        },
    },
})
