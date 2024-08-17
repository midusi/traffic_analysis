<script>
import axios from 'axios'

export default {
  data() {
    return {
      servicios: [],
      selectedService: '',
      searchText: '',
      tiposServicios: [],
      paginaActual: 1,
      pagina: 1,
      elementosPorPagina: 6,
      totalElementos: 0,
      loaded: true,
      errors: []
    }
  },
  methods: {
    filtrar() {
      this.loaded = false
      axios
        .get(`${this.$urlGlobal}api/services/search`, {
          params: {
            q: this.searchText,
            type: this.selectedService,
            page: 1,
            per_page: this.elementosPorPagina
          }
        })
        .then((response) => {
          this.servicios = response.data.data
          this.totalElementos = response.data.total
          this.paginaActual = 1
          this.loaded = true
        })
        .catch((e) => {
          this.errors.push(e)
        })
    },
    cargarPagina(pagina) {
      this.loaded = false
      axios
        .get(`${this.$urlGlobal}api/services/search`, {
          params: {
            q: '',
            type: '',
            page: pagina,
            per_page: this.elementosPorPagina
          }
        })
        .then((response) => {
          this.servicios = response.data.data
          this.paginaActual = pagina
          this.loaded = true
        })
        .catch((e) => {
          this.errors.push(e)
        })
    }
  },
  computed: {
    totalPaginas() {
      return Math.ceil(this.totalElementos / this.elementosPorPagina)
    }
  },

  created() {
    this.loaded = false

    axios
      .get(`${this.$urlGlobal}api/services/types`)
      .then((response) => {
        this.tiposServicios = response.data.data.map((tipo) => tipo.nombre)
      })
      .catch((e) => {
        this.errors.push(e)
      })
    axios
      .get(`${this.$urlGlobal}api/services/search`, {
        params: {
          q: '',
          type: '',
          page: 1,
          per_page: this.elementosPorPagina
        }
      })
      .then((response) => {
        this.servicios = response.data.data
        this.totalElementos = response.data.total
        this.loaded = true
      })
      .catch((e) => {
        this.errors.push(e)
      })
  }
}
</script>

<template>
  <div class="flex justify-center">
    <div class="bg-stone-100 p-10 rounded-lg shadow-lg text-center">
      <h1 class="text-5xl font-bold text-gray-800 pb-16">Servicios</h1>
      <div class="flex justify-end mb-4">
        <select
          v-model="selectedService"
          id="tipoServicio"
          name="tipoServicio"
          class="w-full md:w-auto px-3 py-1 rounded my-1 md:m-0 md:rounded-none md:rounded-l-lg border md:border-r-0 border-zinc-400 focus:ring-2 focus:ring-sky-200"
        >
          <option value="">Todos los servicios</option>
          <option v-for="service in tiposServicios" :key="service" :value="service">
            {{ service }}
          </option>
        </select>
        <input
          v-model="searchText"
          type="text"
          id="servicio"
          name="servicio"
          class="w-full md:w-auto px-3 py-1 rounded md:rounded-none my-1 md:m-0 border md:border-r-0 focus:ring-2 border-zinc-400 focus:ring-sky-200"
        />
        <button
          @click="filtrar()"
          class="block mx-auto md:m-0 md:inline bg-[var(--blue-secondary)] hover:bg-[var(--blue-primary)] focus:ring-4 focus:ring-sky-200 px-3 py-1 text-white rounded-lg md:rounded-none md:rounded-r-lg border border-[var(--blue-secondary)]"
        >
          Filtrar
        </button>
      </div>

      <div
        v-if="this.servicios.length > 0"
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
      >
        <div
          v-for="service in this.servicios"
          :key="service.id"
          class="p-4 border rounded-lg shadow bg-white"
        >
          <h2 class="text-xl font-semibold">{{ service.nombre }}</h2>
          <p class="text-gray-500">
            {{ service.institucion.nombre }} - <i>{{ service.tipo.nombre }}</i>
          </p>
          <p class="text-gray-500">{{ service.descripcion }}</p>
          <p class="mt-2">
            <span
              v-for="tag in service.palabras_claves"
              :key="tag"
              class="mr-2 bg-[var(--blue-accent)] text-[var(--indigo-primary)] px-2 py-1 rounded-full"
            >
              {{ tag }}
            </span>
          </p>
          <button
            type="button"
            class="mt-2 p-1 text-sm font-medium text-[var(--blue-secondary)] bg-white disabled:opacity-40 border border-gray-200 rounded-lg enabled:hover:bg-gray-200 hover:text-[var(--blue-primary)] focus:z-10 focus:ring-2 focus:ring-[var(--indigo-primary)] focus:text-[var(--indigo-primary)]"
          >
            <router-link :to="{ name: 'service', params: { id: service.id } }"
              >+ ver más</router-link
            >
          </button>
        </div>
      </div>
      <div v-else-if="!this.loaded"><span class="loader"></span></div>
      <div v-else class="justify-center p-10">No hay resultados para tu búsqueda 😓</div>

      <div class="mt-4">
        <button
          @click="cargarPagina(paginaActual - 1)"
          :disabled="paginaActual === 1"
          type="button"
          class="px-4 py-2 text-sm font-medium text-[var(--blue-primary)] bg-white disabled:opacity-40 border border-gray-200 rounded-s-lg enabled:hover:bg-gray-200 hover:tex-[var(--indigo-primary)] focus:z-10 focus:ring-2 focus:ring-[var(--indigo-primary)] focus:text-[var(--indigo-primary)]"
        >
          Anterior
        </button>

        <button
          @click="cargarPagina(paginaActual + 1)"
          :disabled="paginaActual === totalPaginas"
          type="button"
          class="px-4 py-2 text-sm font-medium text-[var(--blue-primary)] bg-white disabled:opacity-40 border border-gray-200 rounded-e-lg enabled:hover:bg-gray-200 hover:text-[var(--indigo-primary)] focus:z-10 focus:ring-2 focus:ring-[var(--indigo-primary)] focus:text-[var(--indigo-primary)]"
        >
          Siguiente
        </button>
        <p class="mt-1 text-xs text-[var(--indigo-primary)]">
          Página {{ paginaActual }} de {{ totalPaginas }}
        </p>
      </div>

      <ul v-if="errors && errors.length">
        <li v-for="(error, index) in errors" :key="index">
          {{ error.message }}
        </li>
      </ul>
    </div>
  </div>
</template>
