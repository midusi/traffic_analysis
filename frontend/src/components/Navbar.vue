<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">
        <img src="../assets/Analisis_de_transito.png" alt="Logo" width="150" height="50" />
      </a>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <a class="nav-link fw-semibold" href="#" style="color: #ffffff">Inicio</a>
          </li>
          <li class="nav-item">
            <a class="nav-link fw-semibold" href="#" style="color: #ffffff">Videos</a>
          </li>
          <li class="nav-item" v-if="authStore.isAuthenticated && authStore.user.admin">
            <a class="nav-link fw-semibold" href="#" style="color: #ffffff">Panel admin</a>
          </li>
          <!-- Condicional para mostrar el botón basado en la autenticación -->
          <li class="nav-item" v-if="!authStore.isAuthenticated">
            <a class="btn text-white" style="background-color: #0b5757" href="#" @click="goToLogin">Iniciar Sesión</a>
          </li>
          <li class="nav-item" v-else>
            <a class="btn text-white" style="background-color: #0b5757" href="#" @click="logout">Cerrar Sesión</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { useAuthStore } from '@/stores/auth'
import router from '@/router'

export default {
  name: "Navbar",
  setup() {
    const authStore = useAuthStore();

    const goToLogin = () => {
      router.push({ name: 'login' });
    };

    const logout = async () => {
      await authStore.logoutUser();
      router.push({ name: 'login' });
    };

    return {
      authStore,
      goToLogin,
      logout,
    };
  },
};
</script>

<style scoped>
.navbar {
  background-color: #0b5757 !important; /* Color oscuro principal */
}

.nav-link:hover {
  color: #a7c4c4 !important; /* Efecto hover más claro */
}

.navbar-brand img {
  object-fit: contain;
}
</style>
