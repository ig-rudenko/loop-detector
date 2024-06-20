<template>
  <Menu/>

  <div class="py-5">
    <h1 class="flex justify-content-center align-items-center gap-3">
      <i class="text-blue-500 pi pi-telegram text-4xl"/> Telegram оповещения
    </h1>
    <div class="justify-content-center gap-2">
      <AddNewTelegramNotification :notification-service="telegramService" @created="getTelegramNotifications"/>
      <TelegramNotification v-for="n in telegramNotifications"
                            :notification="n" :notificationService="telegramService"
                            @update="getTelegramNotifications"/>
    </div>
  </div>

</template>

<script lang="ts">
import {defineComponent} from 'vue';
import Menu from '@/components/Menu.vue';
import LoopPreviewCard from "@/components/LoopPreviewCard.vue";
import {TelegramNotificationsService, TgNotification} from "@/services/telegramNotifications";
import TelegramNotification from "@/components/TelegramNotification.vue";
import AddNewTelegramNotification from "@/components/AddNewTelegramNotification.vue";

export default defineComponent({
  name: "Notifications",
  components: {AddNewTelegramNotification, TelegramNotification, LoopPreviewCard, Menu},
  data() {
    return {
      tgService: {} as TelegramNotificationsService,
      telegramNotifications: [] as TgNotification[],
    }
  },

  mounted() {
    this.getTelegramNotifications()
    this.tgService = new TelegramNotificationsService();
  },

  computed: {
    telegramService(): TelegramNotificationsService {
      return <TelegramNotificationsService>this.tgService
    }
  },

  methods: {
    getTelegramNotifications() {
      this.tgService.getNotifications().then(
          value => this.telegramNotifications = value
      )
    },
  }
})
</script>

<style scoped>

</style>