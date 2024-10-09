<template>
    <div v-if="datos.data != null">
        <button type="button" class="btn btn-outline-primary btn-sm" @click="probandoCosas()">Apreta aca a ver si funca</button>
        <BaseTable v-bind:datos="datos" :titulo='`Pruebas`' @changePage="getData" />
    </div>
</template>

<script>
import BaseTable from '../base/table/BaseTable.vue';
import { apiService, getCookie } from '@/services/api';

export default {
    components: {
        BaseTable,
    },

    data() {
        return {
            datos: {
                data: null,
                columns: [
                    { key: 'name', label: "Nombre" },
                ],
            },
            persona: null,
            errors: [],
        }
    },

    async created() {
        this.getData(1, 5);
    },

    methods: {
        async getData(page, perPage) {
            try {
                const response = await apiService.get(import.meta.env.VITE_API_URL + "/prueba", {
                    params: {
                        page: page,
                        per_page: perPage,
                    },
                });
                this.datos.data = response.data;
            } catch (error) {
                this.errors.push(error);
            }
        },

        async probandoCosas() {
            try {
                const response = await apiService.get("auth/logout", {
                    headers: {
                        'X-CSRF-TOKEN': getCookie('csrf_access_token'),
                    }
                });
                if(response.status == 200) {
                    this.$toast.success("Se deslogueo joya, booooca booooooca")    
                }
            } catch(error) {
                this.$toast.error(error)
            }
        },
    },

}
</script>