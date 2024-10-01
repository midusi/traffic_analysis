<script setup>
import Navbar from './components/Navbar.vue'
import { RouterView } from 'vue-router'
</script>

<template>
  <header>
    <Navbar />
  </header>

  <div class="main">
    <RouterView />
  </div>
</template>
