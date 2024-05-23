<template>
  <Toast/>
  <router-view/>
  <video id="background-video" autoplay loop muted poster="/img/back-graph-preview.png">
    <source src="/img/background-white-graph.mp4" type="video/mp4">
  </video>
</template>

<script setup>
import Toast from "primevue/toast";
</script>
