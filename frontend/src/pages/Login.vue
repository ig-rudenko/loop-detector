<script lang="ts">
import {defineComponent} from 'vue'
import LoginForm from "@/components/LoginForm.vue";

export default defineComponent({
  name: "Login",
  components: {LoginForm},
  mounted() {
    document.title = "Вход | Ecstasy-Loop"
    // const body: HTMLBodyElement = document.getElementsByTagName("body")[0];
    // body.classList.add('body-back-image')
  },

})
</script>

<template>
  <video id="background-video" autoplay loop muted poster="/img/back-graph-preview.png">
    <source src="/img/background-white-graph.mp4" type="video/mp4">
  </video>
  <div class="flex justify-content-center align-items-center pt-7">
    <LoginForm/>
  </div>
</template>

<style>
#background-video {
  height: 100vh;
  width: 100vw;
  object-fit: cover;
  position: fixed;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  z-index: -1;
  user-select: none;
}

.body-back-image {
  background-image: url("/img/back-waves.jpg");
  background-position: center center;
  background-repeat: no-repeat;
  background-size: cover;
  background-attachment: fixed;
}
</style>