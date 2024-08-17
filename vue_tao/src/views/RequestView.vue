<template>
  <div class="flex justify-left">
    <div class="bg-stone-100 p-10 rounded-lg shadow-lg text-left relative">
      <h1 class="text-5xl font-bold text-gray-800 pb-16">Solicitar Servicio: {{ servicio ? servicio.nombre : 'Cargando...'
      }}</h1>
      <div v-if="servicio">
        <form @submit.prevent="submitSolicitud">
          <div>
            <label for="detalle">Detalle:</label>
            <input name="detalle" type="text" id="detalle" v-model="solicitud.detalle" required
              class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50" />
          </div>
          <div>
            <input name="file" type="file" @change="uploadFile" ref="file" class="mt-4">

          </div>
          <div>
            <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded-lg mt-2">Solicitar</button>
          </div>
        </form>
      </div>
      <div v-else>
        <p class="mt-4">Cargando información del servicio...</p>
      </div>
      <div v-if="errors.length" class="mt-4">
        <p>Se produjo un error al cargar el servicio:</p>
        <ul>
          <li v-for="error in errors" :key="error" class="text-red-500">{{ error }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { fetchWrapper } from '../helpers';
import { useAuthStore } from '../stores/auth.store';
import router from '../router'

export default {
  data() {
    return {
      servicio: null,
      solicitud: {
        detalle: '',
        archivos_adjuntos: '',
        anotaciones: ''
      },
      errors: []
    };
  },
  created() {
    axios.get(`https://admin-grupo14.proyecto2023.linti.unlp.edu.ar/api/services/${this.$route.params.id}`)
      .then(response => {
        console.log(response.data);
        this.servicio = response.data;
      })
      .catch(e => {
        this.errors.push(e);
      });
    fetchWrapper.get(`https://admin-grupo14.proyecto2023.linti.unlp.edu.ar/api/me/requests/estado/1`)
      .then(res => {
        console.log(res);
        this.estado = res;
      })
      .catch(e => {
        this.errors.push(e);
      });
  },

  methods: {
    uploadFile(event) {
      //const files = event.target.files;
      //this.solicitud.archivos_adjuntos = files;
      this.solicitud.archivos_adjuntos = event.target.files[0];

    },


    submitSolicitud() {
      const fechaActual = new Date().toISOString();

      const formData = new FormData();
      formData.append('detalle', this.solicitud.detalle);
      formData.append('nombre_servicio', this.servicio.nombre);
      formData.append('servicio_id', this.servicio.id);
      formData.append('file', this.solicitud.archivos_adjuntos);
      formData.append('usuario_id', useAuthStore().getUserId())

      // Enviar la solicitud al servidor
      axios.post('https://admin-grupo14.proyecto2023.linti.unlp.edu.ar/api/me/requests/cargar/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
        .then(response => {
          console.log(response.data);
          console.log("EXITO!!!")
          router.push('/requests')
        })
        .catch(error => {
          console.error(error);
          console.log("Fallo 😔");
          flash("Solicitud realizada con exito!","success")
        });
    },
  },
};
</script>