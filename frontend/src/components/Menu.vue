<script lang="ts">
import {defineComponent} from 'vue'
import {mapActions} from "vuex";

export default defineComponent({
  name: "Menu",

  data() {
    return {
      logoutDialogVisible: false,
    }
  },

  methods: {
    ...mapActions("auth", ["logout"]),
    performLogout() {
      this.logout()
      this.logoutDialogVisible = false;
      document.location.href = "/";
    },
  }
})
</script>

<template>
  <div class="flex py-1 my-1 justify-content-between">
    <Button icon="pi pi-home" outlined label="Главная" severity="primary"></Button>

    <Button @click="logoutDialogVisible=true" outlined icon="pi pi-sign-out" label="Выйти" severity="warning"></Button>
  </div>

  <Dialog v-model:visible="logoutDialogVisible" class="pt-2" :show-header="false" modal :style="{ width: '25rem' }">
      <div class="flex align-items-center py-4">
        <i class="text-5xl pi pi-exclamation-circle mr-2" />
        <h3>Вы уверены, что хотите выйти?</h3>
      </div>

    <div class="flex justify-content-end gap-2">
      <Button type="button" severity="primary" outlined label="Остаться" @click="logoutDialogVisible = false"></Button>
      <Button type="button" severity="danger" outlined label="Выйти" @click="performLogout"></Button>
    </div>
  </Dialog>


</template>

<style scoped>

</style>