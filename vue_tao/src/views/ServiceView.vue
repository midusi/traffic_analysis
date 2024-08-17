<script>
import axios from 'axios';
import { useAuthStore } from '../stores/auth.store';
export default {
  data() {
    return {
      servicio: null, // Inicializa servicio como null
      user: null,
      errors: [],
    };
  },
  created() {
    axios.get(`https://admin-grupo14.proyecto2023.linti.unlp.edu.ar/api/services/${this.$route.params.id}`)
      .then(response => {
        console.log(response.data);
        this.servicio = response.data;
      })
      .catch(error => {
        this.errors.push(error);
      });

    // Obtener el usuario de useAuthStore de manera asíncrona
    // El resultado podría no estar disponible de inmediato
    // depending on how useAuthStore is implemented
    this.user = useAuthStore().user;
    if (this.user) {
      console.log(this.user);
    }
  },
};
</script>

<template>
  <div class="flex justify-left">
    <div class="bg-stone-100 p-10 rounded-lg shadow-lg text-left relative">
      <h1 class="text-5xl font-bold text-gray-800 pb-16">Detalles del Servicio</h1>
      <div v-if="servicio">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <ul>
            <li>
              <h2 class="text-xl font-semibold">{{ servicio.nombre }}</h2>
            </li>
            <li>
              <p>{{ servicio.descripcion }}</p>
            </li>
            <li>
              <p>{{ servicio.tipo ? servicio.tipo.nombre : '' }}</p>
            </li>
            <li>
              <p class="mt-2">
                <span v-for="tag in servicio.palabras_claves" :key="tag"
                  class="mr-2 bg-[var(--blue-accent)] text-[var(--indigo-primary)] px-2 py-1 rounded-full">
                  {{ tag }}
                </span>
              </p>
            </li>
          </ul>
        </div>
      </div>
      <div v-else>
        <p>Cargando información del servicio...</p>
      </div>
      <div>
        <!-- Botón "Solicitar" -->
        <div v-if="user">
          <button type="button"
            class="absolute top-12 right-4 p-4 text-white bg-blue-500 rounded-full shadow-lg hover:bg-blue-600 focus:outline-none">
            <router-link v-if="servicio" :to="{ name: 'request', params: { id: servicio.id } }">
              Solicitar
            </router-link>
          </button>
        </div>
        <div v-else>
          <button type="button"
            class="absolute top-12 right-4 p-4 text-white bg-blue-500 rounded-full shadow-lg hover:bg-blue-600 focus:outline-none">
            <router-link :to="{ name: 'login' }">Solicitar</router-link>
          </button>
        </div>
      </div>
      <div v-if="errors.length">
        <p>Se produjo un error al cargar el servicio:</p>
        <ul>
          <li v-for="error in errors" :key="error">{{ error }}</li>
        </ul>
      </div>
    </div>
  </div>

  <!-- Detalle de la institucion -->
  <div class="flex justify-left">
    <div class="bg-stone-100 p-10 rounded-lg shadow-lg text-left mt-4">
      <h1 class="text-5xl font-bold text-gray-800 pb-16">Detalles de la institución del servicio</h1>
      <div v-if="servicio && servicio.institucion">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <ul>
            <li>
              <h2 class="text-xl font-semibold">{{ servicio.institucion.nombre }}</h2>
            </li>
            <li>
              <h2>{{ servicio.institucion.info }}</h2>
            </li>
            <li>
              <h2>{{ servicio.institucion.direccion }}</h2>
            </li>
          </ul>
        </div>
      </div>
      <div v-else>
        <p>No se está imprimiendo la institución</p>
      </div>
    </div>
  </div>
</template>





