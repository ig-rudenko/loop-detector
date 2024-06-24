<template>

  <div class="text-xl pb-2">
    VLAN, где замечена петля:
  </div>

  <div class="flex gap-3">
    <div v-for="info in getVlansInfo()">
      <Badge severity="info" style="font-size: 1rem;">v{{info[0]}}</Badge> Кол-во: {{info[1]}}
    </div>
  </div>

</template>

<script lang="ts">
import {defineComponent, PropType} from "vue";
import {MessagesAnalyzer} from "@/services/messages.analyzer.ts";
import {DetailMessage} from "@/types.ts";

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
      const data = this.msgAnalyzer.getVlansInfo()
      console.log("getVlansInfo")
      console.log(data)
      return data
    }
  }
})

</script>

<style scoped>

</style>