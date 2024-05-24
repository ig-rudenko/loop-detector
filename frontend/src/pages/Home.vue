<template>
  <Menu/>

  <div class="pt-5">
    <h1 class="text-center">Список петель, которые хранятся</h1>
  </div>
  <div v-if="storedGraphs" v-for="info in storedGraphs"
       class="flex gap-3 flex-wrap justify-content-center align-items-center">
    <LoopPreviewCard class="cursor-pointer" @click="$router.push('/loop/stored/'+info.name)" :info="info"/>
  </div>

</template>

<script lang="ts">
import {defineComponent} from 'vue';
import Menu from "@/components/Menu.vue";
import {mapState} from "vuex";
import {GraphService, StoredGraphFile} from "@/services/graph.ts";
import LoopPreviewCard from "@/components/LoopPreviewCard.vue";

export default defineComponent({
  name: "Home",
  components: {LoopPreviewCard, Menu},
  mounted() {
    document.title = "Ecstasy-Loop";
    if (!this.loggedIn) {
      this.$router.push("/login");
      return
    }
    this.getStoredLoopGraphs()
  },

  data() {
    return {
      storedGraphs: null as StoredGraphFile[] | null,
      graphService: new GraphService(this.$toast),
    }
  },

  computed: {
    ...mapState({
      loggedIn: (state: any) => state.auth.status.loggedIn,
      user: (state: any) => state.auth.user,
    }),
  },

  methods: {
    getStoredLoopGraphs(): void {
      this.graphService.getStoredGraphs().then(data => this.storedGraphs = data);
    },
  }
})
</script>

<style scoped>

</style>