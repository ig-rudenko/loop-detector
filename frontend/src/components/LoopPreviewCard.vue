<template>
  <div class="border-round p-5 h-full max-w-25rem zoomin hover:shadow-5 bg-white-alpha-50 hover:bg-white-alpha-80">
    <div class="flex gap-2 font-bold text-xl mb-2 align-items-center">
      <i class="pi pi-share-alt text-xl"></i>
      {{ info.name }}
    </div>
    <div>{{ modTime }}</div>
  </div>
</template>

<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {StoredGraphFile} from "@/services/graph.ts";

export default defineComponent({
  name: "LoopPreviewCard",
  props: {
    info: {required: true, type: Object as PropType<StoredGraphFile>}
  },

  computed: {
    modTime() {
      const date = new Date(this.info.modTime)
      return date.toLocaleString()
    }
  }

})
</script>

<style scoped>

</style>