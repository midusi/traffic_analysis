<template>
    <div v-if="datos.data != null">
        <BaseTable v-bind:datos="datos" :titulo='`Pruebas`' @changePage="getData" />
    </div>
</template>

<script>
import BaseTable from '../base/table/BaseTable.vue';
import { apiService } from '@/services/api';

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
    },

}
</script>