<script>
import { fetchWrapper } from '../helpers'

export default {
  props: ['id'],
  mounted() {
    this.getSolicitud()
  },
  data() {
    return {
      nuevoContenido: '',
      showAddAnotacion: false,
      // datos harcodeados porque no andan las peticiones c/autenticación
      solicitud: null
    }
  },
  methods: {
    getSolicitud() {
      fetchWrapper.get(`${this.$urlGlobal}api/me/requests/${this.id}`).then((res) => {
        this.solicitud = res
      })
    },
    formatearFecha(fecha) {
      const agregarCero = (num) => {
        return num > 9 ? num : `0${num}`
      }
      const date = new Date(fecha)

      const dia = date.getDate()
      const mes = date.getMonth() + 1
      const anio = date.getFullYear()
      const horas = date.getHours()
      const minutos = date.getMinutes()

      const fechaFormateada = `${agregarCero(dia)}/${agregarCero(mes)}/${anio}`
      const horaFormateada = `${agregarCero(horas)}:${agregarCero(minutos)}`

      return `${fechaFormateada} ${horaFormateada}`
    },
    agregarClasesAnotacion(anotacion) {
      if (anotacion.publicado_por === 'Cliente') return 'float-right bg-[var(--blue-light)]'
      else if (anotacion.publicado_por === 'Institución') return 'float-left bg-zinc-200'
    },
    addAnotacion(e) {
      fetchWrapper
        .post(`${this.$urlGlobal}api/me/requests/${this.id}/notes`, {
          text: this.nuevoContenido
        })
        .then((res) => {
          console.log(res)
        })
    }
  }
}
</script>

<template>
  <div v-show="showAddAnotacion" id="anotacion-modal" tabindex="-1" aria-hidden="true"
    class="flex overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-50 justify-center items-center min-w-full bg-zinc-800 bg-opacity-50 md:inset-0 h-[calc(100%-1rem)] min-h-full">
    <div id="anotacion-modal" class="relative p-4 lg:w-1/3 max-h-full">
      <div class="relative bg-white rounded-lg shadow">
        <!-- Modal header -->
        <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t">
          <h3 class="text-xl font-semibold text-gray-900 uppercase tracking-wide">
            Agregar anotación
          </h3>
          <button type="button"
            class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center"
            @click="showAddAnotacion = false">
            <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6" />
            </svg>
            <span class="sr-only">Cerrar ventana</span>
          </button>
        </div>
        <!-- Modal body -->
        <form @submit.prevent="addAnotacion">
          <div class="p-4 md:p-5 space-y-4">
            <textarea class="rounded w-full border border-zinc-400 p-2" name="contenido" style="resize: none"
              v-model="nuevoContenido" placeholder="Escriba el contenido de la anotación..."></textarea>
          </div>
          <!-- Modal footer -->
          <div class="flex items-center p-4 md:p-5 border-t border-gray-200 rounded-b">
            <button type="submit" :disabled="!nuevoContenido"
              class="transition disabled:opacity-60 disabled:text-[var(--blue-secondary)] enabled:text-white border border-[var(--blue-secondary)] enabled:bg-[var(--blue-secondary)] enabled:hover:bg-[var(--blue-primary)] enabled:focus:ring-4 enabled:focus:outline-none enabled:focus:ring-blue-300 font-medium rounded-lg text-sm px-3 py-2 text-center">
              Agregar
            </button>

            <button type="button" @click="showAddAnotacion = false"
              class="ms-3 text-gray-500 bg-white hover:bg-gray-100 focus:ring-4 focus:outline-none focus:ring-blue-300 rounded-lg border border-zinc-400 text-sm font-medium px-3 py-2 hover:text-gray-900 focus:z-10">
              Cancelar
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>

  <div class="mx-auto p-5 md:w-2/3">
    <router-link to="/requests" class="text-[var(--blue-secondary)] underline group">
      <p class="group-hover:translate-x-[0.5rem] transition">Volver a tus solicitudes</p>
    </router-link>

    <div v-if="solicitud" class="bg-stone-100 rounded-lg my-3 p-5 shadow-lg w-full">
      <h1 class="text-2xl">
        Solicitud para
        <span class="font-semibold uppercase">"{{ solicitud.servicio.nombre }}"</span>
      </h1>

      <div class="grid lg:grid-cols-2 my-5 gap-2">
        <div>
          <h3 class="text-xl font-semibold uppercase mb-2">Información</h3>
          <p>
            La solicitud fue creada el
            {{
              new Date(solicitud.fecha_creacion)
                .toJSON()
                .slice(0, 10)
                .split('-')
                .reverse()
                .join('/')
            }}.
          </p>

          <p>
            Su estado actual es
            <span class="font-semibold">{{
              solicitud.estado_actual.nombre }}</span>
          </p>

          <p class="my-3">
            Detalle: <span class="font-semibold uppercase">{{ solicitud.detalle }}</span>.
          </p>

          <h3 class="mt-5 uppercase font-semibold">Historial de cambios</h3>

          <div class="overflow-y-scroll h-[16rem] my-2 flex flex-col border-l-2 border-[var(--blue-secondary)] xl:w-3/4">
            <div v-for="(item, index) in solicitud.cambios_estado" :key="index"
              class="bg-[var(--blue-light)] rounded-lg border-b border-zinc-400 p-4 m-2 shadow-md">
              <p class="text-sm font-light">{{ formatearFecha(item.fecha) }}</p>
              <h4>
                Tu solicitud pasó al estado
                <span class="text-base font-semibold">{{ item.estado.nombre }}</span>.
              </h4>

              <p class="mt-2">Comentarios de la institución:</p>
              <p class="font-light italic">"{{ item.comentario }}"</p>
            </div>
          </div>
        </div>
        <div>
          <div class="grid md:grid-cols-2 mb-2">
            <h3 class="text-xl font-semibold uppercase">Anotaciones</h3>
            <div>
              <button type="button"
                class="float-right text-white border border-[var(--blue-secondary)] bg-[var(--blue-secondary)] hover:bg-[var(--blue-primary)] focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-3 py-2 text-center"
                @click="($event) => (showAddAnotacion = true)">
                Agregar
              </button>
            </div>
          </div>
          <div class="anotaciones-container flex h-full">
            <div v-if="solicitud.anotaciones.length > 0" class="w-full overflow-y-scroll h-[25rem]">
              <div v-for="(item, index) in solicitud.anotaciones" :index="index"
                class="w-3/4 rounded-lg border border-zinc-300 shadow m-2 p-3" :class="agregarClasesAnotacion(item)">
                <p class="font-semibold">{{ item.publicado_por }}</p>
                <textarea disabled style="resize: none"
                  class="bg-zinc-100 p-2 my-1 rounded border-zinc-300 border font-light w-full">{{ item.contenido }}</textarea>
                <p class="text-sm font-light float-right">{{ formatearFecha(item.fecha) }}</p>
              </div>
            </div>
            <div v-else
              class="mx-auto opacity-60 rounded-lg my-[6rem] p-5 border-2 border-[var(--blue-secondary)] h-fit text-center">
              <div class="flex">
                <svg width="89px" height="89px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"
                  class="mx-auto stroke-[var(--blue-secondary)]">
                  <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                  <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
                  <g id="SVGRepo_iconCarrier">
                    <path
                      d="M12 16.99V17M12 7V14M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z"
                      stroke-width="1" stroke-linecap="round" stroke-linejoin="round"></path>
                  </g>
                </svg>
              </div>
              <p>Esta solicitud todavía no tiene anotaciones.</p>
              <p>
                Las anotaciones son comentarios útiles para mantenerte en contacto con la
                institución.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
