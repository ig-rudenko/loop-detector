<script lang="ts">
import {defineComponent} from 'vue'
import {mapActions, mapState} from "vuex";

import {LoginUser} from "@/services/user";
import {AxiosError, AxiosResponse} from "axios";
import getVerboseAxiosError from "@/errorFmt";

export default defineComponent({
  name: "LoginForm",

  data() {
    return {
      user: new LoginUser(),
      userError: "",
    };
  },
  computed: {
    ...mapState({
      loggedIn: (state: any) => state.auth.status.loggedIn,
    }),
  },
  created() {
    if (this.loggedIn) {
      this.$router.push("/");
    }
  },
  methods: {
    ...mapActions("auth", ["login"]),

    getClassesFor(isValid: boolean): string[] {
      return isValid ? ['w-full', 'pb-3', 'bg-white-alpha-90'] : ['w-full', 'pb-3', 'p-invalid']
    },

    handleLogin() {
      this.login(this.user)
          .then(
              (value: AxiosResponse|AxiosError) => {
                if (value.status == 200) {
                  this.$router.push("/");
                } else {
                  this.userError = (<AxiosError>value).message
                }
              },
              () => this.userError = 'Неверный логин или пароль'
          )
          .catch(
          (reason: AxiosError<any>) => {
            this.userError = getVerboseAxiosError(reason)
          }
      );
    },

  },
})
</script>

<template>
  <div class="bg-white-alpha-80 p-5 flex flex-wrap justify-content-center align-items-center border-round">

<!--    <div class="px-4">-->
<!--      <img src="/img/logo.jpg" alt="Image" height="512" class="mb-2 image-logo" />-->
<!--    </div>-->

    <div class="w-full max-w-23rem">
      <div class="text-center mb-3">
        <div class="text-900 text-3xl font-medium mb-3 flex flex-wrap justify-content-center">
          <div>Пожалуйста, войдите в </div>
          <div class="flex align-items-center justify-content-center gap-2">
            <img src="/img/ecstasy-logo.png" alt="Image" height="32" class="mb-2 pi-spin" />
            <div class="pb-2">Ecstasy-Loop</div>
          </div>
        </div>
      </div>

      <div>
        <div v-if="userError.length" class="flex justify-content-center">
          <InlineMessage @click="userError = ''" severity="error"><span v-html="userError"></span></InlineMessage>
        </div>

        <div class="mb-3">
          <label for="username-input" class="block text-900 font-medium mb-2">Username</label>
          <InputText @keydown.enter="handleLogin" v-model="user.username" id="username-input" type="text" autofocus :class="getClassesFor(user.valid.username)" />
        </div>

        <div class="mb-3">
            <label for="password-input" class="block text-900 font-medium mb-2">Password</label>
            <InputText @keydown.enter="handleLogin" v-model="user.password" id="password-input" type="password" :class="getClassesFor(user.valid.password)" />
        </div>

        <div class="mb-3">
          <a class="font-medium no-underline ml-2 text-black text-right cursor-pointer">Forgot password?</a>
        </div>

        <Button label="Sign In" icon="pi pi-user" severity="info" @click="handleLogin" class="w-full"></Button>
      </div>
    </div>
  </div>
</template>

<style scoped>

@media (width < 600px) {
  .image-logo {
    height: 300px!important;
  }
}

.hover-opacity-100:hover {
  opacity: 1.0!important;
}

</style>