<script>
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  Title,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'
import { Pie, Bar } from 'vue-chartjs'
import { fetchWrapper } from '../helpers'

ChartJS.register(ArcElement, Tooltip, Legend, Title, BarElement, CategoryScale, LinearScale)

export default {
  components: {
    Pie,
    Bar
  },
  methods: {
    getStatsData() {
      fetchWrapper.get(`${this.$urlGlobal}api/stats/`).then((res) => {
        console.log(res)
        this.pieData = {
          labels: Object.values(res.solicitudes_por_estado).map((i) => i.nombre),
          datasets: [
            {
              backgroundColor: [
                'rgb(251 191 36)',
                'rgb(167 139 250)',
                'rgb(220 38 38)',
                'rgb(56 189 248)',
                'rgb(74 222 128)',
                'rgb(63 63 70)'
              ],
              data: Object.values(res.solicitudes_por_estado).map((i) => i.count)
            }
          ]
        }

        this.barData = {
          labels: Object.values(res.servicios_mas_solicitados).map((i) => i.nombre),
          datasets: [
            {
              label: 'Cantidad de solicitudes',
              backgroundColor: '#81c3d7',
              data: Object.values(res.servicios_mas_solicitados).map((i) => i.count)
            }
          ]
        }

        this.rankingInstituciones = res.instituciones_mas_solicitadas
        this.loaded = true
      })
    },
    setClassById(id) {
      if (this.rankingInstituciones.length === 1) return 'rounded-lg'

      if (id === 0) return 'rounded-t-lg'
      else if (id === this.rankingInstituciones.length - 1) return 'rounded-b-lg border-t-0'
      else return 'border-t-0'
    }
  },
  mounted() {
    this.getStatsData()
  },
  data() {
    return {
      loaded: false,
      pieData: null,
      barData: null,
      rankingInstituciones: null,
      pieOptions: {
        mantainAspectRatio: false
      }
    }
  }
}
</script>

<template>
  <div class="w-full flex">
    <div class="mx-auto bg-stone-100 p-5 md:w-3/4 rounded-lg shadow-lg">
      <h1 class="text-2xl font-semibold uppercase">Análisis de datos</h1>

      <div v-if="loaded" class="my-3 grid lg:grid-cols-2 gap-4">
        <div>
          <div class="text-center my-3">
            <h3 class="text-xl font-semibold uppercase">Solicitudes agrupadas por estado</h3>

            <div class="flex">
              <div class="mx-auto">
                <Pie :data="pieData" :options="pieOptions" />
              </div>
            </div>
          </div>

          <div class="text-center my-3">
            <h3 class="text-xl font-semibold uppercase">Servicios más solicitados</h3>

            <div class="flex">
              <div class="mx-auto">
                <Bar :data="barData" />
              </div>
            </div>
          </div>
        </div>

        <div>
          <h3 class="text-xl font-semibold uppercase">Instituciones con más solicitudes</h3>

          <div class="mx-2 my-3">
            <ol class="list-decimal list-inside">
              <li
                v-for="(item, index) in rankingInstituciones"
                :index="index"
                class="border border-zinc-300 text-lg p-2 tracking-wide"
                :class="setClassById(index)"
              >
                <span class="font-semibold">{{ item.nombre }}</span> ({{ item.count }}
                {{ item.count > 1 ? 'solicitudes' : 'solicitud' }})
              </li>
            </ol>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
