<template>
    <div v-if="datos.data != null" class="table-responsive table-content border rounded-2 shadow mt-3">
        <h2 class="fw-bolder ms-1">{{ titulo }}</h2>
        <ContentTable :columns="datos.columns" :rows="datos.data.pruebas" />
        <div class="d-flex flex-row justify-content-center align-items-center">
            <div class="d-flex flex-row ms-auto align-items-center me-3">
                <div class="d-flex flex-row align-items-center mb-3 me-2 column-gap-3">
                    <label>Filas por página: </label>
                    <input class="form-control-sm" type="number" name="per_page" id="per_page" min="1"
                        v-model="perPage" :max="datos.data.total" @input="$emit('changePage', 1, this.perPage)" />
                    <p class="mb-0">{{ datos.data.first + "-" + datos.data.last + " de " + datos.data.total }}</p>
                </div>
                <nav class="ms-5 me-2" aria-label="Page navigation example">
                    <ul class="pagination">
                        <li @click="$emit('changePage', datos.data.page - 1, this.perPage)"
                            :class="{ 'disabled': !datos.data.has_prev }" class="page-item">
                            <a class="page-link border border-0" href="#" aria-label="Previous">
                                <span aria-hidden="true">&laquo;</span>
                            </a>
                        </li>
                        <li @click="$emit('changePage', datos.data.page + 1, this.perPage)"
                            :class="{ 'disabled': !datos.data.has_next }" class="page-item">
                            <a class="page-link border border-0" href="#" aria-label="Next">
                                <span aria-hidden="true">&raquo;</span>
                            </a>
                        </li>
                    </ul>
                </nav>
            </div>
        </div>
    </div>
</template>

<script>
import ContentTable from './ContentTable.vue'

export default {
    components: {
        ContentTable,
    },
    props: {
        titulo: "",
        datos: {},
    },

    data() {
        return {
            page: 1,
            perPage: 5,
            rows: [],
        }
    },
}
</script>