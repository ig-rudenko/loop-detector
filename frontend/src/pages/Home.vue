<template>
  <Menu/>

  <Welcome/>

</template>

<script  lang="ts">
import Menu from "@/components/Menu.vue";
import Welcome from "@/components/Welcome.vue";
import {defineComponent} from "vue";
import {mapState} from "vuex";

export default defineComponent({
  name: "Home",
  components: {Welcome, Menu},
  async beforeMount() {
    document.title = "Ecstasy-Loop";
    if (!this.loggedIn) await this.$router.push("/login")
  },
  computed: {
    ...mapState({
      loggedIn: (state: any) => state.auth.status.loggedIn,
    }),
  },
});
</script>
