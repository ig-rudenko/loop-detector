<template>
  <div class="border-round p-5 h-full max-w-25rem zoomin hover:shadow-5 bg-white-alpha-50 hover:bg-white-alpha-80 relative"
       :class="cardClasses">
    <!--DELETE-->
    <div v-if="user?.isSuperuser" class="absolute" style="right: 0; top: 0">
      <Button @click="showModalDelete=true" severity="danger" outlined size="small" icon="pi pi-trash"/>
    </div>

    <!--NAME-->
    <div @click="$router.push('/loop/stored/'+info.name)"
         class="flex gap-2 font-bold text-xl mb-2 align-items-center cursor-pointer">
      <i class="pi pi-share-alt text-xl"></i>
      {{ info.name }}
    </div>
    <div class="py-2"><i class="pi pi-calendar mr-2"/>{{ modTime }}</div>

    <div v-if="graphInfo" class="flex flex-wrap gap-1">
      <div v-for="vlan in graphInfo.vlans">
        <Badge severity="danger" class="text-sm">v{{ vlan.vid }}</Badge>
        <small class="text-sm">/{{ vlan.count }}</small>
      </div>
    </div>
    <InlineMessage v-if="graphInfoError" v-tooltip.top="graphInfoError">Ошибка загрузки `info`</InlineMessage>
  </div>

  <Dialog v-model:visible="showModalDelete" class="pt-2" :show-header="false" modal :style="{ width: '25rem' }">
    <div class="flex flex-wrap">
      <div class="flex align-items-center pt-5">
        <i class="text-5xl pi pi-exclamation-circle mr-2"/>
        <h3 class="m-0 p-0">Вы уверены, что хотите удалить {{info.name}}?</h3>
      </div>
      <div class="py-3 text-xl">Данное действие невозможно будет обратить</div>
    </div>

    <div class="flex justify-content-end gap-2">
      <Button type="button" severity="primary" outlined label="Нет" @click="showModalDelete = false"></Button>
      <Button type="button" severity="danger" outlined label="Удалить" @click="deleteLoop"></Button>
    </div>
  </Dialog>

</template>

<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {StoredGraphFile} from "@/services/graph.ts";
import api from "@/services/api.ts";
import errorFmt from "@/errorFmt.ts";
import {mapState} from "vuex";

interface GraphInfo {
  messagesCount: number
  vlans: { vid: number, count: number }[]
}

export default defineComponent({
  name: "LoopPreviewCard",
  props: {
    info: {required: true, type: Object as PropType<StoredGraphFile>}
  },

  emits: ["delete"],

  data() {
    return {
      graphInfo: null as GraphInfo | null,
      graphInfoError: "",
      showModalDelete: false
    }
  },

  mounted() {
    api.get<GraphInfo>("/graph-info/" + this.info.name).then(
        value => this.graphInfo = value.data
    ).catch(
        reason => this.graphInfoError = errorFmt(reason)
    )
  },

  computed: {
    ...mapState({
      loggedIn: (state: any) => state.auth.status.loggedIn,
      user: (state: any) => state.auth.user,
    }),
    cardClasses() {
      if (!this.graphInfo) return [];
      if (this.graphInfo.messagesCount > 1500) return ["border-3", "border-red-600"];
      if (this.graphInfo.messagesCount > 1000) return ["border-2", "border-red-400"];
      if (this.graphInfo.messagesCount > 500) return ["border-2", "border-orange-400"];
    },
    modTime() {
      const date = new Date(this.info.modTime)
      return date.toLocaleString()
    }
  },


  methods: {
    deleteLoop() {
      this.$emit("delete");
      this.showModalDelete = false;
    }
  }

})
</script>

<style scoped>

</style>