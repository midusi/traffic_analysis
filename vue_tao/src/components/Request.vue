<script>
    export default {
        props: ['item'],
        methods: {
            getBackgroundByEstado(id) {
                switch (id) {
                    case 1:
                        return 'bg-amber-400';
                    case 2:
                        return 'bg-violet-400';
                    case 3:
                        return 'bg-red-600';
                    case 4:
                        return 'bg-sky-400';
                    case 5:
                        return 'bg-green-400';
                    case 6:
                        return 'bg-zinc-700';
                }
            }
        }
    }

    
</script>

<template>
    <div class="grid grid-cols-2 mb-3">
        <div>
            <h2 class="text-xl font-bold uppercase tracking-wide">{{ item.servicio.nombre }}</h2>
        </div>
        <div>
            <p class="float-right
            rounded-full px-2 text-white font-semibold text-sm"
            :class="getBackgroundByEstado(item.estado_actual.id)">● {{  item.estado_actual.nombre }}</p>
        </div>
    </div>
    <p class="font-light">Creada el {{  new Date(item.fecha_creacion).toJSON().slice(0,10).split('-').reverse().join('/') }}</p>

    <p><span class="font-semibold">Detalle:</span> {{ item.detalle }}</p>
    <router-link :to="{ name: 'show-request', params: { id: item.id} }">
        <button
        type="button"
        class="mt-2 p-1 text-sm font-medium
                text-[var(--blue-secondary)] bg-white disabled:opacity-40 border border-gray-200 rounded-lg enabled:hover:bg-gray-200 hover:text-[var(--blue-primary)] focus:z-10 focus:ring-2 focus:ring-[var(--indigo-primary)] focus:text-[var(--indigo-primary)]">
        + ver más
        </button>
    </router-link>
</template>