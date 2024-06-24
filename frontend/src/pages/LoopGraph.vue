<template>
  <Menu/>
  <div v-if="graphData" class="pt-3 border-round bg-white-alpha-50">
    <h2 class="text-center mb-0">Граф петли из истории - "{{storedGraphName}}"</h2>
    <div class="flex flex-wrap py-2 pl-4 gap-2">
      <ButtonGroup>
        <Button icon="pi pi-list" label="Все сообщения" @click="showMessagesDialog" severity="secondary"/>
      </ButtonGroup>
    </div>

    <div class="py-2 pl-4 gap-2">
      <MessagesInfo v-if="messages.length" :messages="messages" />
    </div>
    <Graph :graph-data="graphData"/>
  </div>

  <div v-else>
    Loading...
  </div>

  <Dialog v-model:visible="visibleMessagesDialog" header="Все сообщения" maximizable class="w-full">
    <FullMessagesTable :messages="messages"/>
  </Dialog>

</template>

<script lang="ts">
import {defineComponent} from 'vue'
import {mapState} from "vuex";

import {GraphData, GraphService} from "@/services/graph";
import Graph from "@/components/Graph.vue";
import Menu from "@/components/Menu.vue";
import FullMessagesTable from "@/components/FullMessagesTable.vue";
import {DetailMessage} from "@/types.ts";
import api from "@/services/api.ts";
import {AxiosError} from "axios";
import getVerboseAxiosError from "@/errorFmt.ts";
import MessagesInfo from "@/components/MessagesInfo.vue";

export default defineComponent({
  name: "LoopGraph",
  components: {MessagesInfo, FullMessagesTable, Graph, Menu},

  data() {
    return {
      graphData: null as GraphData | null,
      graphService: new GraphService(this.$toast),

      visibleMessagesDialog: false,
      messages: [] as DetailMessage[],
    }
  },


  mounted() {
    document.title = this.storedGraphName + " | Ecstasy-Loop"
    if (!this.loggedIn) {
      this.$router.push("/login")
      return
    }
    this.getGraphData()
    this.getMessages()
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

    getMessages(): void {
      api.get<DetailMessage[]>("/messages/stored/" + this.storedGraphName)
          .then(value => {
            this.messages = value.data
          })
          .catch((error: AxiosError) => this.toastError(error))
    },

    showMessagesDialog(): void {
      this.visibleMessagesDialog = true
    },

    toastError(error: AxiosError) {
      this.$toast.add({
        severity: 'error',
        summary: 'Error',
        detail: getVerboseAxiosError(error),
        life: 5000
      })
    }

  }
})
</script>

<style scoped>

</style>