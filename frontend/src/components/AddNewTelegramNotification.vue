<template>
  <div v-if="!showForm" class="flex justify-content-center">
    <Button @click="showForm=true" severity="info" label="Добавить" text icon="pi pi-plus-circle"/>
  </div>

  <div v-else class="flex justify-content-center my-3">
    <Card class="p-3" style="width: 33rem;">
      <template #header>
        <div class="flex justify-content-end"><Button @click="showForm=false" severity="danger" text icon="pi pi-times"/></div>
      </template>
      <template #content>
        <div class="mb-2">
          <div class="flex-auto">
            <label for="new-chat-id" class="font-bold block mb-2">Название</label>
            <InputText id="new-chat-id" style="font-family: monospace" v-model="name" class="w-full"/>
          </div>
        </div>
        <div class="mb-2">
          <div class="flex-auto">
            <label for="new-chat-id" class="font-bold block mb-2">Токен</label>
            <InputText id="new-chat-id" type="password" style="font-family: monospace" v-model="token" class="w-full"/>
          </div>
        </div>
        <div class="mb-2">
          <div class="flex-auto">
            <label for="new-chat-id" class="font-bold block mb-2">Описание</label>
            <Textarea id="new-chat-id" style="font-family: monospace" v-model="description" rows="6" class="w-full"/>
          </div>
        </div>

        <Button severity="success" label="Создать" outlined @click="create" />

      </template>
    </Card>
  </div>
</template>

<script lang="ts">
import {defineComponent, PropType} from 'vue';
import {TelegramNotificationsService} from "@/services/telegramNotifications";
import Textarea from "primevue/textarea";

export default defineComponent({
  name: "AddNewTelegramNotification",
  components: {Textarea},
  props: {
    notificationService: {required: true, type: Object as PropType<TelegramNotificationsService>}
  },
  emits: ["created"],
  data() {
    return {
      showForm: false,

      name: "",
      token: "",
      description: ""
    }
  },

  methods: {
    clearForm() {
      this.name = ""
      this.token = ""
      this.description = ""
    },
    create() {
      this.notificationService.addBot(this.name, this.token, this.description).then(
          () => {
            this.$emit("created");
            this.showForm = false;
            this.clearForm();
          }
      )
    }
  }
});

</script>

<style scoped>

</style>