<script lang="ts">
import {defineComponent} from 'vue'
import LoginForm from "@/components/LoginForm.vue";

export default defineComponent({
  name: "Login",
  components: {LoginForm},
  mounted() {
    document.title = "Вход | Ecstasy-Loop"
    const body: HTMLBodyElement = document.getElementsByTagName("body")[0];
    console.log(body)
    body.classList.add('body-back-image')
  },

})
</script>

<template>
  <div class="flex justify-content-center align-items-center pt-7">
    <LoginForm/>
  </div>
</template>

<style>
.body-back-image {
  background-image: url("/img/back-waves.jpg");
  background-position: center center;
  background-repeat: no-repeat;
  background-size: cover;
  background-attachment: fixed;
}
</style>