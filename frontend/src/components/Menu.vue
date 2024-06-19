<script lang="ts">
import {defineComponent} from 'vue'
import {mapActions, mapState} from "vuex";
import OverlayPanel from "primevue/overlaypanel";
import UserDetail from "@/components/UserDetail.vue";

export default defineComponent({
  name: "Menu",
  components: {UserDetail},

  data() {
    return {
      logoutDialogVisible: false,
    }
  },

  computed: {
    ...mapState({
      loggedIn: (state: any) => state.auth.status.loggedIn,
      user: (state: any) => state.auth.user,
    }),
    currentURL() {
      return this.$route.path
    }
  },

  methods: {
    ...mapActions("auth", ["logout"]),
    performLogout() {
      this.logout()
      this.logoutDialogVisible = false;
      document.location.href = "/";
    },

    toggleUserDetail(event: Event): void {
      (<OverlayPanel>this.$refs.userDetail).toggle(event, event.target)
    }
  }
})
</script>

<template>
  <div class="flex py-1 my-1 justify-content-between align-items-start">
    <div class="gap-1 flex flex-wrap">
      <Button icon="pi pi-home" @click="$router.push('/')" label="Главная" raised
              :severity="currentURL=='/'?'contrast':'secondary'"></Button>
      <Button icon="pi pi-spinner" @click="$router.push('/currentLoop')" label="Текущая" raised
              :severity="currentURL=='/currentLoop'?'contrast':'secondary'"></Button>
      <Button v-if="user" @click="toggleUserDetail" icon="pi pi-user" :label="user.username" raised
              severity="secondary"/>
      <Button v-if="user && user.isSuperuser" @click="$router.push('/notifications')" icon="pi pi-bell"
              label="Оповещения" raised :severity="currentURL=='/notifications'?'contrast':'secondary'"/>
    </div>

    <OverlayPanel ref="userDetail">
      <UserDetail :user="user"/>
    </OverlayPanel>

    <Button @click="logoutDialogVisible=true" text icon="pi pi-sign-out" label="Выйти" severity="warning"></Button>
  </div>

  <Dialog v-model:visible="logoutDialogVisible" class="pt-2" :show-header="false" modal :style="{ width: '25rem' }">
    <div class="flex align-items-center py-4">
      <i class="text-5xl pi pi-exclamation-circle mr-2"/>
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