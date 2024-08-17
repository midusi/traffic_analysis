<script>
import Request from '../components/Request.vue'
import { fetchWrapper } from '../helpers'

export default {
  components: {
    Request
  },
  data() {
    return {
      sort: 'fecha_creacion',
      order: 'desc',
      url: `${this.$urlGlobal}api/me/requests/?`,
      data: null,
      solicitudes: null
    }
  },
  methods: {
    filtrarSolicitudes(e) {
      this.getSolicitudes()
    },
    getSolicitudes() {
      fetchWrapper
        .get(
          this.url +
            new URLSearchParams({
              sort: this.sort,
              order: this.order,
              page: this.solicitudes?.page || 1
            })
        )
        .then((res) => {
          this.solicitudes = res
        })
    },
    getNext() {
      if (this.solicitudes.has_next) {
        this.solicitudes.page += 1
        this.getSolicitudes()
      }
    },
    getPrev() {
      if (this.solicitudes.has_previous) {
        this.solicitudes.page -= 1
        this.getSolicitudes()
      }
    }
  },
  mounted() {
    this.getSolicitudes()
  }
}
</script>

<template>
  <div class="w-full flex">
    <div class="mx-auto bg-stone-100 p-5 md:w-3/4 rounded-lg shadow-lg">
      <h1 class="text-2xl font-semibold uppercase">Solicitudes</h1>

      <div class="mx-2 my-4 flex">
        <form @submit.prevent="filtrarSolicitudes">
          <p for="sort" class="block" role="label">Ordenar por:</p>

          <select
            id="sort"
            name="sort"
            class="w-full md:w-auto px-3 py-1 rounded my-1 md:m-0 md:rounded-none md:rounded-l-lg border md:border-r-0 border-zinc-400 focus:ring-2 focus:ring-sky-200"
            v-model="sort"
          >
            <option value="fecha_creacion">Fecha de creación</option>
            <option value="estado_id">Estado</option>
            <option value="detalle">Detalle</option>
            <option value="servicio_id">Servicio</option>
          </select>

          <select
            id="order"
            name="order"
            class="w-full md:w-auto px-3 py-1 rounded md:rounded-none my-1 md:m-0 border md:border-r-0 focus:ring-2 border-zinc-400 focus:ring-sky-200"
            v-model="order"
          >
            <option value="desc">Descendiente</option>
            <option value="asc">Ascendiente</option>
          </select>

          <button
            type="submit"
            class="block mx-auto md:m-0 md:inline bg-[var(--blue-secondary)] hover:bg-[var(--blue-primary)] focus:ring-4 focus:ring-sky-200 px-3 py-1 text-white rounded-lg md:rounded-none md:rounded-r-lg border border-[var(--blue-secondary)]"
          >
            Buscar
          </button>
        </form>
      </div>
      <div
        v-if="solicitudes && solicitudes.data.length > 0"
        class="container mx-auto grid lg:grid-cols-3"
      >
        <div
          v-for="(item, index) in solicitudes.data"
          :key="index"
          class="p-4 border rounded-lg shadow bg-white m-2"
        >
          <Request :item="item" />
        </div>
      </div>
      <div
        v-else
        class="mx-auto opacity-60 rounded-lg p-5 h-fit text-center text-[var(--blue-primary)] font-semibold"
      >
        <div class="flex">
          <svg
            width="89px"
            height="89px"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            class="mx-auto stroke-[var(--blue-secondary)]"
          >
            <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
            <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
            <g id="SVGRepo_iconCarrier">
              <path
                d="M12 16.99V17M12 7V14M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z"
                stroke-width="1"
                stroke-linecap="round"
                stroke-linejoin="round"
              ></path>
            </g>
          </svg>
        </div>
        <p>Todavía no enviaste ninguna solicitud.</p>
      </div>
      <div v-if="solicitudes" class="flex flex-col my-3 text-center">
        <div class="rounded-md shadow-sm mx-auto" role="group">
          <button
            type="button"
            @click="getPrev"
            :disabled="!solicitudes.has_previous"
            class="px-4 py-2 text-sm font-medium text-gray-900 bg-white border border-gray-200 disabled:opacity-60 rounded-s-lg enabled:hover:bg-gray-100 enabled:hover:text-[var(--blue-secondary)]"
          >
            Anterior
          </button>
          <button
            type="button"
            @click="getNext"
            :disabled="!solicitudes.has_next"
            class="px-4 py-2 text-sm font-medium text-gray-900 bg-white border border-gray-200 disabled:opacity-60 rounded-e-lg enabled:hover:bg-gray-100 enabled:hover:text-[var(--blue-secondary)]"
          >
            Siguiente
          </button>
        </div>
        <p>
          Página {{ solicitudes.page }} de {{ Math.ceil(solicitudes.total / solicitudes.per_page) }}
        </p>
      </div>
    </div>
  </div>
</template>
