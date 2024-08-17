<script>
// send a request to 127.0.0.1/api/me/profile and show the data in the template
import axios from 'axios'
import { fetchWrapper } from '../helpers'

export default {
  data() {
    return {
      user: null,
      loading: true
    }
  },
  mounted() {
    // Realiza la petición a la API cuando el componente se monta
    this.fetchUserProfile()
  },
  methods: {
    fetchUserProfile() {
      // Realiza la petición a la API usando Axios
      fetchWrapper
        .get(`${this.$urlGlobal}api/me/profile`)
        .then((response) => {
          // Al recibir la respuesta, actualiza los datos del usuario y detén el indicador de carga
          console.log(response)
          this.user = response || {}
          this.loading = false
        })
        .catch((error) => {
          console.error('Error al obtener el perfil del usuario:', error)
          this.loading = false
        })
    }
  }
}
</script>

<template>
  <div>
    <h1>User Profile</h1>
    <div v-if="loading">Cargando...</div>
    <div v-else-if="!user || Object.keys(user).length === 0">
      No se encontraron datos de usuario.
    </div>
    <div v-else>
      <div v-for="(value, key) in user" :key="key">
        <p>{{ key }}: {{ value }}</p>
      </div>
    </div>
  </div>
</template>
