<template>
  <Image :src="graphLink" preview/>
</template>

<script lang="ts">
import {defineComponent} from 'vue';

export default defineComponent({
  name: "GraphImage",
  computed: {
    graphLink() {
      return "";
    }
  }
})
</script>

<style scoped>

</style>