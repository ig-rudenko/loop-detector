<template>
  <Menu/>

  <div class="py-5">
    <h1 class="flex justify-content-center align-items-center gap-3">
      <i class="text-blue-500 pi pi-telegram text-4xl"/> Telegram оповещения
    </h1>
    <div class="justify-content-center gap-2">
      <AddNewTelegramNotification :notification-service="tgService" @created="getTelegramNotifications"/>
      <TelegramNotification v-for="n in telegramNotifications"
                            :notification="n" :notification-service="tgService" @update="getTelegramNotifications"/>
    </div>
  </div>

</template>

<script lang="ts">
import {defineComponent} from 'vue';
import Menu from '@/components/Menu.vue';
import LoopPreviewCard from "@/components/LoopPreviewCard.vue";
import {TelegramNotificationsService, TgNotification} from "@/services/telegramNotifications.ts";
import TelegramNotification from "@/components/TelegramNotification.vue";
import AddNewTelegramNotification from "@/components/AddNewTelegramNotification.vue";

export default defineComponent({
  name: "Notifications",
  components: {AddNewTelegramNotification, TelegramNotification, LoopPreviewCard, Menu},
  data() {
    return {
      tgService: new TelegramNotificationsService(),
      telegramNotifications: [] as TgNotification[],
    }
  },

  mounted() {
    this.getTelegramNotifications()
  },

  methods: {
    getTelegramNotifications()  {
      this.tgService.getNotifications().then(
          value => this.telegramNotifications = value
      )
    },
  }
})
</script>

<style scoped>

</style>