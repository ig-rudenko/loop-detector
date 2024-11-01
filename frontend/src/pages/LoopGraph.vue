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
import {mapState} from "vuex";
import {defineComponent} from 'vue';

import Menu from "@/components/Menu.vue";
import Graph from "@/components/Graph.vue";
import MessagesInfo from "@/components/MessagesInfo.vue";
import FullMessagesTable from "@/components/FullMessagesTable.vue";
import {DetailMessage} from "@/types";
import {GraphData, graphService} from "@/services/graph";
import messagesService from "@/services/messages.service";

export default defineComponent({
  name: "LoopGraph",
  components: {MessagesInfo, FullMessagesTable, Graph, Menu},

  data() {
    return {
      graphData: null as GraphData | null,

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
    getGraphData() {
      graphService.getStoredGraph(this.storedGraphName).then(data => this.graphData = data);
    },

    getMessages() {
      messagesService.getGraphMessages(this.storedGraphName).then(value => this.messages = value)
    },

    showMessagesDialog() {
      this.visibleMessagesDialog = true
    },

  }
})
</script>

<style scoped>

</style>