<template>
  <Menu/>
  <div v-if="graphData && graphData.nodes?.length" class="pt-3 border-round bg-white-alpha-50">
    <div class="flex flex-row align-items-center py-2 pl-4 gap-2">
      <div style="font-size: 1.2rem;">Глубина графа</div>
      <SelectButton :allow-empty="false" @change="getGraphData" v-model="depth" :options="[1, 2, 3]"/>
      <Button label="Все сообщения" outlined @click="showMessagesDialog"/>
      <Button v-if="user?.isSuperuser" @click="visibleDeleteMessages=true" icon="pi pi-trash" label="Удалить сообщения"
              severity="danger" outlined/>
    </div>
    <Graph :graph-data="graphData"/>
  </div>
  <div v-else>
    <h1 class="text-center">В данный момент</h1>
    <h1 class="text-center">нет петель на сети!</h1>
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

  <Dialog v-model:visible="visibleMessagesDialog" header="Все сообщения">
    <FullMessagesTable :messages="currentMessages"/>
  </Dialog>

</template>

<script lang="ts">
import {defineComponent} from 'vue';
import Graph from "@/components/Graph.vue";
import Menu from "@/components/Menu.vue";
import {GraphData, GraphService} from "@/services/graph";
import {mapState} from "vuex";
import FullMessagesTable from "@/components/FullMessagesTable.vue";
import api from "@/services/api.ts";
import {DetailMessage} from "@/types.ts";
import getVerboseAxiosError from "@/errorFmt.ts";
import {AxiosError} from "axios";

export default defineComponent({
  name: "LoopGraph",
  components: {FullMessagesTable, Graph, Menu},

  data() {
    return {
      graphData: null as GraphData | null,
      depth: 1,
      graphService: new GraphService(this.$toast),

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
    getGraphData(): void {
      this.graphService.getCurrentGraph(this.depth).then(data => this.graphData = data);
    },

    showMessagesDialog() {
      if (!this.currentMessages.length) this.getCurrentMessages();
      this.visibleMessagesDialog = true;
    },

    getCurrentMessages() {
      api.get<DetailMessage[]>("/messages/")
          .then(value => this.currentMessages = value.data)
          .catch(
              (error: AxiosError) => {
                this.$toast.add({
                  severity: 'error',
                  summary: 'Error',
                  detail: getVerboseAxiosError(error),
                  life: 5000
                })
              }
          )
    },

    deleteCurrentMessages() {
      api.delete("/messages/").then(
          () => {
            this.$toast.add({
              severity: 'success',
              summary: 'Удалено',
              detail: "Все сообщения были удалены",
              life: 5000
            })
          }
      )
          .catch(
              (error: AxiosError) => {
                this.$toast.add({
                  severity: 'error',
                  summary: 'Error',
                  detail: getVerboseAxiosError(error),
                  life: 5000
                })
              }
          )
    }
  }
})
</script>

<style scoped>
</style>