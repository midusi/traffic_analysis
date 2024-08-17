<script>
import { useAuthStore } from '@/stores/auth.store'
import router from '../router'
export default {
  data() {
    return {
      isOpen: false,
      auth: useAuthStore
    }
  },
  methods: {
    cerrarSesion() {
      useAuthStore().logout()
    }
  }
}
</script>

<template>
  <header
    class="bg-[var(--blue-primary)] sm:flex sm:justify-between sm:items-center sm:px-4 sm:py-3"
  >
    <div class="flex items-center justify-between px-4 py-3 sm:p-0">
      <div>
        <img class="h-8" src="./icons/logos/cidepint.png" alt="CIDEPINT" />
      </div>
      <div class="sm:hidden">
        <button @click="isOpen = !isOpen" type="button" class="block text-white focus:outline-none">
          <svg class="h-6 w-6 fill-current" viewBox="0 0 24 24">
            <path
              v-if="isOpen"
              fill-rule="evenodd"
              d="M18.278 16.864a1 1 0 0 1-1.414 1.414l-4.829-4.828-4.828 4.828a1 1 0 0 1-1.414-1.414l4.828-4.829-4.828-4.828a1 1 0 0 1 1.414-1.414l4.829 4.828 4.828-4.828a1 1 0 1 1 1.414 1.414l-4.828 4.829 4.828 4.828z"
            />
            <path
              v-if="!isOpen"
              fill-rule="evenodd"
              d="M4 5h16a1 1 0 0 1 0 2H4a1 1 0 1 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2z"
            />
          </svg>
        </button>
      </div>
    </div>
    <nav :class="isOpen ? 'block' : 'hidden'" class="px-2 pt-2 pb-4 sm:flex sm:p-0">
      <RouterLink
        to="/"
        class="block px-2 py-1 text-white font-semibold rounded hover:bg-gray-800 group"
      >
        <p class="group-hover:-translate-y-[2px] transition">Home</p>
      </RouterLink>

      <RouterLink
        to="/search"
        class="block px-2 py-1 text-white font-semibold rounded hover:bg-gray-800 group"
      >
        <p class="group-hover:-translate-y-[2px] transition">Servicios</p>
      </RouterLink>

      <RouterLink
        to="/requests"
        class="block px-2 py-1 text-white font-semibold rounded hover:bg-gray-800 group"
      >
        <p class="group-hover:-translate-y-[2px] transition">Solicitudes</p>
      </RouterLink>

      <RouterLink v-if="this.auth().getUserRole()"
        to="/stats"
        class="block px-2 py-1 text-white font-semibold rounded hover:bg-gray-800 group"
      >
        <p class="group-hover:-translate-y-[2px] transition">Estadísticas</p>
      </RouterLink>

      <RouterLink
        v-if="!this.auth().user"
        to="/login"
        class="block text-[var(--blue-primary)] text-base rounded px-2 py-1 font-semibold group bg-white ml-1"
      >
        <p class="">Acceder</p>
      </RouterLink>
      <button
        v-else
        @click="cerrarSesion()"
        class="block text-[var(--blue-primary)] text-base rounded px-2 py-1 font-semibold group bg-white ml-1"
      >
        <p class="">Cerrar sesión</p>
      </button>
    </nav>
  </header>
</template>
