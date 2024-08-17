<script setup>
import Navbar from './components/Navbar.vue'
</script>

<template>
  <header>
    <Navbar />
  </header>

  <div class="main">
    <RouterView />
  </div>
</template>
