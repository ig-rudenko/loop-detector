<script lang="ts">

import {mapState} from "vuex";
import {defineComponent} from 'vue';

import Menu from "@/components/Menu.vue";
import Welcome from "@/components/Welcome.vue";
import LoopPreviewCard from "@/components/LoopPreviewCard.vue";
import {graphService, PaginatedStoredGraphInfo} from "@/services/graph";
import GraphsHistoryChart, {HistoryItem} from "@/components/GraphsHistoryChart.vue";

export default defineComponent({
  name: "Home",
  components: {GraphsHistoryChart, Welcome, LoopPreviewCard, Menu},
  data() {
    return {
      storedGraphs: null as PaginatedStoredGraphInfo | null,
      currentPage: 1,
      perPage: 25,
      history: [] as HistoryItem[]
    }
  },

  mounted() {
    document.title = "Ecstasy-Loop";
    if (!this.loggedIn) {
      this.$router.push("/login");
      return
    }
    this.getStoredLoopGraphs(this.currentPage, this.perPage)

    graphService.getGraphsHistory().then(data => {
      data.forEach(value => this.history.push({datetime: value.modTime, name: value.name}))
    })
  },

  computed: {
    ...mapState({
      loggedIn: (state: any) => state.auth.status.loggedIn,
      user: (state: any) => state.auth.user,
    }),
  },

  methods: {
    getStoredLoopGraphs(page: number, perPage: number): void {
      graphService.getStoredGraphsInfoPage(page, perPage).then(data => this.storedGraphs = data);
    },
    deleteLoop(loopName: string): void {
      graphService.deleteStoredGraph(loopName).then(
          () => this.getStoredLoopGraphs(1, this.perPage)
      )
    }
  }
})
</script>

<template>
  <Menu/>

  <div class="py-5">

    <GraphsHistoryChart v-if="history.length" :data="history"/>

    <h1 class="text-center">Список петель, которые хранятся</h1>
    <div v-if="storedGraphs" class="flex py-4 gap-3 flex-wrap justify-content-center ">
      <LoopPreviewCard v-for="info in storedGraphs.results" :graph-data="info" @delete="deleteLoop(info.name)"/>
    </div>
    <div v-else class="flex justify-content-center">
      <div class="p-5 border-dashed border-1 border-round shadow-2">Пока нет хранимых данных</div>
    </div>

    <div v-if="storedGraphs" class="flex justify-content-center">
      <Paginator @page="p => getStoredLoopGraphs(p.page+1, perPage)"
                 @update:rows="value => perPage = value"
                 :rows="perPage" :totalRecords="storedGraphs.count" :rowsPerPageOptions="[10, 25, 50]"></Paginator>
    </div>
  </div>
</template>

<style scoped>

</style>