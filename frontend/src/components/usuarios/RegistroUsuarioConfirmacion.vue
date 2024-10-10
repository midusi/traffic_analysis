<template>
    <section class="vh-100 bg-gradient">
        <div class="container py-5 h-100">
            <div class="row d-flex justify-content-center align-items-center h-100">
                <div class="col-12 col-md-8 col-lg-6 col-xl-5">
                    <form ref="formulario" class="card shadow needs-validation" @submit.prevent="confirmarUsuario" style="border-radius: 1rem;" novalidate>
                        <div class="card-body p-5 text-center">
                            <img src="../../assets/Analisis_de_transito.png" alt="Logo Analisis de transito" width="300"
                                height="120">
                            <h2 class="text-center fw-bold mb-5 mt-3">Registrar usuario</h2>

                            <div class="input-group mt-4 mb-2">
                                <div class="input-group-text" style="background-color: #0b5757">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-lock-fill" viewBox="0 0 16 16">
                                        <path d="M8 1a2 2 0 0 1 2 2v4H6V3a2 2 0 0 1 2-2m3 6V3a3 3 0 0 0-6 0v4a2 2 0 0 0-2 2v5a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2"/>
                                    </svg>
                                </div>
                                <input v-model="password" class="form-control" type="password" minlength="8" maxlength="255" name="password" id="password"
                                    placeholder="Contraseña" required/>
                                <div class="invalid-feedback">
                                    Debe ingresar una contraseña minimo que contenga entre 8 y 255 caracteres.
                                </div>
                            </div>

                            <div class="input-group mt-4 mb-3">
                                <div class="input-group-text" style="background-color: #0b5757">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-lock-fill" viewBox="0 0 16 16">
                                        <path d="M8 1a2 2 0 0 1 2 2v4H6V3a2 2 0 0 1 2-2m3 6V3a3 3 0 0 0-6 0v4a2 2 0 0 0-2 2v5a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2"/>
                                    </svg>
                                </div>
                                <input v-model="password_repetida" class="form-control" type="password" minlength="8" maxlength="255" name="password_repetida" id="password_repetida"
                                    placeholder="Ingrese de nuevo la contraseña" required/>
                                <div class="invalid-feedback">
                                    Debe ingresar la contraseña ingresada anteriormente.
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
    props: {
        token: {
            type: String,
            required: true,
        },
    },

    data() {
        return {
            password: '',
            password_repetida: '',
            errores: [],
        }
    },

    methods: {
        async confirmarUsuario() {
            const form = this.$refs.formulario;

            if (this.contraseña !== this.contraseña_repetida) {
                this.$toast.error("Las contraseñas ingresadas deben ser iguales")
            }

            if (form.checkValidity()) {
                try {                                        
                    await apiService.post("registro/confirmar",
                        {
                            password: this.password,
                            token: this.token,
                        })
                    .then((response) => {
                        if(response.status == 200) {
                            this.$toast.success(response.data.message);
                            this.$router.push("/");
                        }
                    })
                } catch(error) {
                    console.log(error)
                    this.$toast.error(error.response.data.error);
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