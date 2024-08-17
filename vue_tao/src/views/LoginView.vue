<script>
import { useAuthStore } from '@/stores'

export default {
    methods: {
        onSubmit(values) {
            const authStore = useAuthStore()
            return authStore.login(this.email, this.password).catch((error) => {
                if(error === 'UNAUTHORIZED') {
                    this.error = 'Email o contraseña invalidos.'
                } else {
                    this.error = error
                }
            })
        }
    },

    data() {
        return {
            email: '',
            password: '',
            error: null,
        }
    }
}
</script>

<template>
  <form @submit.prevent="onSubmit" class="max-w-md mx-auto mt-8 p-4 bg-white shadow-md rounded-md">
    <div class="mb-4">
      <label for="email" class="block text-gray-700 text-sm font-bold mb-2">Email:</label>
      <input
        name="email"
        type="email"
        id="email"
        v-model="email"
        required
        class="w-full px-3 py-2 border border-gray-300 rounded-md"
      />
    </div>
    <div class="mb-4">
      <label for="password" class="block text-gray-700 text-sm font-bold mb-2">Contraseña:</label>
      <input
        name="password"
        type="password"
        id="password"
        v-model="password"
        required
        class="w-full px-3 py-2 border border-gray-300 rounded-md"
      />
    </div>

   <div class="mb-4 flex justify-center">
      <button
        type="submit"
        class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-gray-700 hover:text-blue-500 hover:font-semibold hover:ring-2 hover:ring-blue-500"
      >
        Iniciar sesión
      </button>

      <a href="https://admin-grupo14.proyecto2023.linti.unlp.edu.ar/autenticacion/registro/" target="_blank"
        class="ml-4 bg-green-500 text-white px-4 py-2 rounded-md hover:bg-gray-700 hover:text-green-500 hover:font-semibold hover:ring-2 hover:ring-green-500">
        Registrarse
      </a>
    </div>

    <div v-if="error" class="text-red-500 mt-2">
      {{ error }}
    </div>
  </form>
</template>
