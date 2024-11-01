<template>

  <div class="text-xl pb-2">
    VLAN, где замечена петля:
  </div>

  <div class="flex flex-wrap gap-x-4 gap-3">
    <div v-for="info in getVlansInfo()">
      <Badge severity="info" style="font-size: 1rem;">v{{info[0]}}</Badge> Кол-во: {{info[1]}}
    </div>
  </div>

</template>

<script lang="ts">
import {defineComponent, PropType} from "vue";

import {DetailMessage} from "@/types";
import {MessagesAnalyzer} from "@/services/messages.analyzer";

export default defineComponent({
  name: "MessagesInfo",
  props: {
    messages: {
      required: true, type: Object as PropType<DetailMessage[]>,
    }
  },

  data() {
      return {
        msgAnalyzer: new MessagesAnalyzer(this.messages),
      }
  },

  methods: {
    getVlansInfo() {
      return this.msgAnalyzer.getVlansInfo()
    }
  }
})

</script>

<style scoped>

</style>