<template>
  <Menu/>
  <Graph :graph-data="graphData"/>
</template>

<script lang="ts">
import {defineComponent} from 'vue'
import Graph from "@/components/Graph.vue";
import Menu from "@/components/Menu.vue";
import {GraphData, GraphService} from "@/services/graph";

export default defineComponent({
  name: "LoopGraph",
  components: {Graph, Menu},

  mounted() {
    document.title = "Ecstasy-Loop"
    // const body: HTMLBodyElement = document.getElementsByTagName("body")[0];
    // body.classList.add('body-back-image')
  },

  computed: {
    graphData(): GraphData {
      return GraphService.getGraph();
    }
  }

})
</script>

<style scoped>
</style>