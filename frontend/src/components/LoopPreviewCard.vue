<template>
  <div class="border-round p-5 h-full max-w-25rem zoomin hover:shadow-5 bg-white-alpha-50 hover:bg-white-alpha-80"
       :class="cardClasses">
    <div class="flex gap-2 font-bold text-xl mb-2 align-items-center">
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
</template>

<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {StoredGraphFile} from "@/services/graph.ts";
import api from "@/services/api.ts";
import errorFmt from "@/errorFmt.ts";

interface GraphInfo {
  messagesCount: number
  vlans: { vid: number, count: number }[]
}

export default defineComponent({
  name: "LoopPreviewCard",
  props: {
    info: {required: true, type: Object as PropType<StoredGraphFile>}
  },

  data() {
    return {
      graphInfo: null as GraphInfo | null,
      graphInfoError: ""
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
  }

})
</script>

<style scoped>

</style>