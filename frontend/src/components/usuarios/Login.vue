<template>
    <section class="vh-100 bg-gradient">
        <div class="container py-5 h-100">
            <div class="row d-flex justify-content-center align-items-center h-100">
                <div class="col-12 col-md-8 col-lg-6 col-xl-5">
                    <form class="card shadow" @submit.prevent="login" style="border-radius: 1rem;">
                        <div class="card-body p-5 text-center">
                            <img src="../../assets/Analisis_de_transito.png" alt="Logo Analisis de transito" width="300"
                                height="120">
                            <h2 class="text-center fw-bold mb-5 mt-3">Iniciar sesión</h2>

                            <div class="input-group mt-4 mb-2">
                                <div class="input-group-text" style="background-color: #0b5757">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                                        class="bi bi-envelope-fill" style="color: white;" viewBox="0 0 16 16">
                                        <path
                                            d="M.05 3.555A2 2 0 0 1 2 2h12a2 2 0 0 1 1.95 1.555L8 8.414.05 3.555ZM0 4.697v7.104l5.803-3.558L0 4.697ZM6.761 8.83l-6.57 4.027A2 2 0 0 0 2 14h12a2 2 0 0 0 1.808-1.144l-6.57-4.027L8 9.586l-1.239-.757Zm3.436-.586L16 11.801V4.697l-5.803 3.546Z" />
                                    </svg>
                                </div>
                                <input v-model="email" class="form-control bg-light" type="text" name="email" id="email"
                                    placeholder="Email" />
                            </div>


                            <div class="input-group mt-1 mb-4">
                                <div class="input-group-text" style="background-color: #0b5757">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                                        class="bi bi-lock-fill" style="color: white;" viewBox="0 0 16 16">
                                        <path
                                            d="M8 1a2 2 0 0 1 2 2v4H6V3a2 2 0 0 1 2-2m3 6V3a3 3 0 0 0-6 0v4a2 2 0 0 0-2 2v5a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2" />
                                    </svg>
                                </div>
                                <input v-model="password" class="form-control bg-light" type="password" name="password"
                                    id="password" placeholder="Contraseña" />
                            </div>


                            <p class="small pb-lg-2">Olvidaste tu contraseña?. <a
                                    class="text-decoration-none fw-semibold" href="#!"
                                    style="color: #0b5757">Recuperar</a></p>

                            <button class="btn text-white w-100 mt-2 fw-semibold shadow-sm" type="submit"
                                :disabled="loading" style="background-color: #0b5757">Iniciar
                                sesión</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
import { mapActions, mapState } from 'pinia'
import { useAuthStore } from '@/stores/auth'

export default {
    data() {
        return {
            email: "",
            password: "",
        };
    },

    computed: {
        ...mapState(useAuthStore, ['loading', 'error']),
    },

    methods: {

        ...mapActions(useAuthStore, ['loginUser']),

        async login() {
            await this.loginUser({ email: this.email, password: this.password });
        },

    },
};
</script>

<style></style>