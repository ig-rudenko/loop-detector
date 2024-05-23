<template>
  <Menu/>
  <div v-if="graphData && graphData.nodes?.length">
    <Graph :graph-data="graphData"/>
  </div>
  <div v-else>
    <h1 class="text-center">В данный момент</h1>
    <h1 class="text-center">нет петель на сети!</h1>
  </div>
</template>

<script lang="ts">
import {defineComponent} from 'vue';
import Graph from "@/components/Graph.vue";
import Menu from "@/components/Menu.vue";
import {GraphData, GraphService} from "@/services/graph";
import {mapState} from "vuex";

export default defineComponent({
  name: "LoopGraph",
  components: {Graph, Menu},

  data() {
    return {
      graphData: null as GraphData|null,
    }
  },

  mounted() {
    document.title = "Текущая петля | Ecstasy-Loop"
    if (!this.loggedIn) {
      this.$router.push("/login")
      return
    }
    this.getGraphData()
  },

  computed: {
    ...mapState({
      loggedIn: (state: any) => state.auth.status.loggedIn,
      user: (state: any) => state.auth.user,
    }),
  },

  methods: {
    getGraphData(): void {
      GraphService.getCurrentGraph().then(data => this.graphData = data);
    },
  }
})
</script>

<style scoped>
</style>