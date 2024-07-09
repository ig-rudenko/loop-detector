<template>
  <Menu/>

  <Welcome/>

  <div class="py-5">
    <h1 class="text-center">Список петель, которые хранятся</h1>
    <div v-if="storedGraphs?.length" class="flex gap-3 flex-wrap justify-content-center align-items-center">
      <LoopPreviewCard v-for="info in storedGraphs" :info="info" @delete="deleteLoop(info.name)"/>
    </div>
    <div v-else class="flex justify-content-center">
      <div class="p-5 border-dashed border-1 border-round shadow-2">Пока нет хранимых данных</div>
    </div>
  </div>

</template>

<script lang="ts">
import {defineComponent} from 'vue';
import Menu from "@/components/Menu.vue";
import {mapState} from "vuex";
import {GraphService, StoredGraphFile} from "@/services/graph.ts";
import LoopPreviewCard from "@/components/LoopPreviewCard.vue";
import Welcome from "@/components/Welcome.vue";

export default defineComponent({
  name: "Home",
  components: {Welcome, LoopPreviewCard, Menu},
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
      this.storedGraphs = []
      this.graphService.getStoredGraphs().then(data => this.storedGraphs = data);
    },
    deleteLoop(loopName: string): void {
      this.graphService.deleteStoredGraph(loopName).then(
          () => this.getStoredLoopGraphs()
      )
    }
  }
})
</script>

<style scoped>

</style>