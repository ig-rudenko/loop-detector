<template>
  <div class="border-round p-5 w-30rem zoomin hover:shadow-5 bg-white-alpha-50 hover:bg-white-alpha-80 relative"
       :class="cardClasses">
    <!--DELETE-->
    <div v-if="user?.isSuperuser" class="absolute" style="right: 0; top: 0">
      <Button @click="showModalDelete=true" severity="danger" outlined size="small" icon="pi pi-trash"/>
    </div>

    <!--NAME-->
    <div @click="$router.push('/loop/stored/'+graphData.name)"
         class="flex gap-2 font-bold text-xl mb-2 align-items-center cursor-pointer">
      <i class="pi pi-share-alt text-xl"></i>
      {{ graphData.name }}
    </div>
    <div class="py-2"><i class="pi pi-calendar mr-2"/>{{ modTime }}</div>

    <div v-if="graphData.info" class="flex flex-wrap gap-2">
      <div v-for="vlan in graphData.info.vlans.sort((a, b) => Number(b.count) - Number(a.count))">
        <Badge severity="danger" class="text-sm">v{{ vlan.vid }}</Badge>
        <small class="text-sm">/{{ vlan.count }}</small>
      </div>
    </div>
  </div>

  <Dialog v-model:visible="showModalDelete" class="pt-2" :show-header="false" modal :style="{ width: '25rem' }">
    <div class="flex flex-wrap">
      <div class="flex align-items-center pt-5">
        <i class="text-5xl pi pi-exclamation-circle mr-2"/>
        <h3 class="m-0 p-0">Вы уверены, что хотите удалить {{graphData.name}}?</h3>
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
import {StoredGraphInfo} from "@/services/graph.ts";
import {mapState} from "vuex";


export default defineComponent({
  name: "LoopPreviewCard",
  props: {
    graphData: {required: true, type: Object as PropType<StoredGraphInfo>}
  },

  emits: ["delete"],

  data() {
    return {
      showModalDelete: false
    }
  },

  computed: {
    ...mapState({
      loggedIn: (state: any) => state.auth.status.loggedIn,
      user: (state: any) => state.auth.user,
    }),
    cardClasses() {
      if (!this.graphData.info) return [];
      if (this.graphData.info.messagesCount > 1500) return ["border-3", "border-red-600"];
      if (this.graphData.info.messagesCount > 1000) return ["border-2", "border-red-400"];
      if (this.graphData.info.messagesCount > 500) return ["border-2", "border-orange-400"];
    },
    modTime() {
      const date = new Date(this.graphData.modTime)
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