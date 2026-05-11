<script setup lang="ts">
</script>

<template>
  <router-view />
</template>

<style>
/* Custom animations if needed, but Tailwind v4 handles most */
@layer base {
  html {
    scroll-behavior: smooth;
  }
}
</style>
