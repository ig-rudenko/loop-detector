<template>
  <Menu/>
  <div class="pt-3 border-round bg-white-alpha-50">
    <div class="flex flex-wrap align-items-center py-2 pl-4 gap-2">
      <div style="font-size: 1.2rem;">Глубина графа</div>
      <SelectButton :allow-empty="false" @change="getGraphData" v-model="depth" :options="[1, 2, 3]"/>
      <ButtonGroup>
        <Button icon="pi pi-list" label="Все сообщения" @click="showMessagesDialog" severity="secondary"/>
        <Button v-if="user?.isSuperuser" @click="visibleDeleteMessages=true" icon="pi pi-trash" severity="danger"/>
      </ButtonGroup>
    </div>

    <div class="py-2 pl-4 gap-2">
      <MessagesInfo v-if="!currentMessages.length" :messages="currentMessages" />
    </div>

    <Graph v-if="!loadingGraphData && graphData && graphData.nodes?.length" :graph-data="graphData"/>
    <div v-else-if="loadingGraphData" class="flex justify-content-center p-3">
      <ProgressSpinner/>
    </div>
    <div v-else-if="!loadingGraphData" class="p-3">
      <h1 class="text-center">В данный момент</h1>
      <h1 class="text-center">нет петель на сети!</h1>
    </div>
  </div>

  <Dialog v-model:visible="visibleDeleteMessages" modal block-scroll
          header="Вы уверены, что хотите удалить все сообщения?">
    <InlineMessage class="mb-2 p-3">
      После удаления, граф будет пресчитан заново и все текущие данные будут потеряны!
    </InlineMessage>
    <div class="flex flex-row gap-2 justify-content-end">
      <Button label="Отмена" autofocus @click="visibleDeleteMessages=false" outlined/>
      <Button label="Удалить" severity="danger" outlined @click="deleteCurrentMessages"/>
    </div>
  </Dialog>

  <Dialog v-model:visible="visibleMessagesDialog" header="Все сообщения"  maximizable class="w-full">
    <FullMessagesTable :messages="currentMessages"/>
  </Dialog>

</template>

<script lang="ts">
import {defineComponent} from 'vue';
import Graph from "@/components/Graph.vue";
import Menu from "@/components/Menu.vue";
import {GraphData, graphService} from "@/services/graph";
import {mapState} from "vuex";
import FullMessagesTable from "@/components/FullMessagesTable.vue";
import api from "@/services/api";
import {DetailMessage} from "@/types.ts";
import getVerboseAxiosError from "@/errorFmt.ts";
import {AxiosError} from "axios";
import MessagesInfo from "@/components/MessagesInfo.vue";
import messagesService from "@/services/messages.service.ts";

export default defineComponent({
  name: "LoopGraph",
  components: {MessagesInfo, FullMessagesTable, Graph, Menu},

  data() {
    return {
      graphData: null as GraphData | null,
      loadingGraphData: true,
      depth: 1,

      visibleMessagesDialog: false,
      currentMessages: [] as DetailMessage[],

      visibleDeleteMessages: false,
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
    getGraphData() {
      this.loadingGraphData = true;
      graphService.getCurrentGraph(this.depth)
          .then(data => {
            this.graphData = data;
            this.loadingGraphData = false;
          })
    },

    showMessagesDialog() {
      if (!this.currentMessages.length) this.getCurrentMessages();
      this.visibleMessagesDialog = true;
    },

    getCurrentMessages() {
      messagesService.getCurrentMessages().then(value => this.currentMessages = value)
    },

    deleteCurrentMessages() {
      messagesService.deleteCurrentMessages()
    },

  }
})
</script>

<style scoped>
</style>