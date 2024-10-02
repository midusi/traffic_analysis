<template>
    <section class="vh-100 bg-gradient">
        <div class="container py-5 h-100">
            <div class="row d-flex justify-content-center align-items-center h-100">
                <div class="col-12 col-md-8 col-lg-6 col-xl-5">
                    <form ref="formulario" class="card shadow needs-validation" @submit.prevent="registrarUsuario" style="border-radius: 1rem;" novalidate>
                        <div class="card-body p-5 text-center">
                            <img src="../../assets/Analisis_de_transito.png" alt="Logo Analisis de transito" width="300"
                                height="120">
                            <h2 class="text-center fw-bold mb-5 mt-3">Registrar usuario</h2>

                            <div class="input-group mt-4 mb-3">
                                <div class="input-group-text" style="background-color: #0b5757">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-fill" viewBox="0 0 16 16">
                                        <path d="M3 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6"/>
                                    </svg>
                                </div>
                                <input v-model="persona.nombre" class="form-control" type="text" pattern="[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+" name="nombre" id="nombre"
                                    placeholder="Nombre" required/>
                                <div class="invalid-feedback">
                                    El nombre es obligatorio y debe poseer solo letras.
                                </div>
                            </div>

                            <!-- Campo para Apellido -->
                            <div class="input-group mb-3">
                                <div class="input-group-text" style="background-color: #0b5757">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-fill" viewBox="0 0 16 16">
                                        <path d="M3 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6"/>
                                    </svg>
                                </div>
                                <input v-model="persona.apellido" class="form-control" type="text" pattern="[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+" name="apellido" id="apellido"
                                    placeholder="Apellido" required />
                                <div class="invalid-feedback">
                                    El apellido es obligatorio y debe poseer solo letras.
                                </div>
                            </div>


                            <div class="input-group mb-3">
                                <div class="input-group-text" style="background-color: #0b5757">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                                        class="bi bi-envelope-fill" style="color: white;" viewBox="0 0 16 16">
                                        <path
                                            d="M.05 3.555A2 2 0 0 1 2 2h12a2 2 0 0 1 1.95 1.555L8 8.414.05 3.555ZM0 4.697v7.104l5.803-3.558L0 4.697ZM6.761 8.83l-6.57 4.027A2 2 0 0 0 2 14h12a2 2 0 0 0 1.808-1.144l-6.57-4.027L8 9.586l-1.239-.757Zm3.436-.586L16 11.801V4.697l-5.803 3.546Z" />
                                    </svg>
                                </div>
                                <input v-model="persona.email" class="form-control" type="email" pattern="[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" name="email" id="email"
                                    placeholder="Email" required/>
                                <div class="invalid-feedback">
                                    Debe ingresar un email con formato 'unusuario@unemail.com'.
                                </div>
                            </div>

                            <div class="input-group mt-1 mb-4">
                                <div class="input-group-text" style="background-color: #0b5757">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                                        class="bi bi-lock-fill" style="color: white;" viewBox="0 0 16 16">
                                        <path
                                            d="M8 1a2 2 0 0 1 2 2v4H6V3a2 2 0 0 1 2-2m3 6V3a3 3 0 0 0-6 0v4a2 2 0 0 0-2 2v5a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2" />
                                    </svg>
                                </div>
                                <input v-model="persona.password" class="form-control" type="password" name="password"
                                    id="password" placeholder="Contraseña" required/>
                                <div class="invalid-feedback">
                                    Debe ingresar una contraseña.
                                </div>
                            </div>

                            <button class="btn text-white w-100 mt-2 fw-semibold shadow-sm" type="submit" style="background-color: #0b5757">Registrar</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
import { apiService } from "@/services/api";

export default {
    data() {
        return {
            persona: {
                nombre: '',
                apellido: '',
                email: '',
                password:''
            }
        }
    },

    methods: {
        async registrarUsuario() {
            const form = this.$refs.formulario;
            console.log()
            if (form.checkValidity()) {
                try {                                        
                    await apiService.post(import.meta.env.VITE_API_URL + "usuarios/registrar",
                        {
                            persona: this.persona,
                        })
                    .then((response) => {
                        if(response.status == 200) {
                            this.$toast.success("Se ha registrado exitosamente");
                            this.$router.push("/");
                        }
                    })
                } catch(error) {
                    this.$toast.error(error);
                    this.errores.push(error);
                }
            } else {
                console.log('Formulario no válido. Realiza acciones adicionales...');
                form.classList.add('was-validated');
            }
        },
    }
}
</script>