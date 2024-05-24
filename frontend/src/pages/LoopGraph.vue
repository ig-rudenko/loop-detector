<template>
  <Menu/>
  <div v-if="graphData" class="pt-3 border-round bg-white-alpha-50">
    <h2 class="text-center">Граф петли из истории</h2>
    <Graph :graph-data="graphData"/>
  </div>

  <div v-else>
    Loading...
  </div>

</template>

<script lang="ts">
import {defineComponent} from 'vue'
import {mapState} from "vuex";

import {GraphData, GraphService} from "@/services/graph";
import Graph from "@/components/Graph.vue";
import Menu from "@/components/Menu.vue";

export default defineComponent({
  name: "LoopGraph",
  components: {Graph, Menu},

  data() {
    return {
      graphData: null as GraphData | null,
      graphService: new GraphService(this.$toast),
    }
  },


  mounted() {
    document.title = this.storedGraphName + " | Ecstasy-Loop"
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
    storedGraphName(): string {
      return this.$route.params.name.toString()
    }
  },

  methods: {
    getGraphData(): void {
      this.graphService.getStoredGraph(this.storedGraphName).then(data => this.graphData = data);
    },
  }
})
</script>

<style scoped>

</style>