<template>

  <div class="flex gap-2 flex-wrap justify-content-center m-2">
    <Card class="p-3 max-w-26rem">
      <template #header>
        <ButtonGroup class="flex justify-content-end">
          <Button v-if="botEditMode" @click="updateBot" size="small" icon="pi pi-check" severity="success"/>
          <Button v-if="botEditMode" @click="botEditMode=false" size="small" icon="pi pi-times" severity="warning"/>
          <Button v-else @click="botEditMode=true" size="small" icon="pi pi-pencil" outlined severity="warning"/>
          <Button @click="deleteBotDialogVisible=true" size="small" icon="pi pi-trash" outlined severity="danger"/>
        </ButtonGroup>
      </template>

      <template #title>
        <div class="flex align-items-center">
          <img :src="'/api/v1/notifications/telegram/'+originalNotificationName+'/avatar'" class="mr-2 border-1 border-300 border-circle"
                  style="width: 128px; height: 128px; z-index: 2" alt="avatar"/>
          <Avatar label="No image" class="mr-2 absolute" style="width: 128px; height: 128px; z-index: 1" shape="circle" />

          <InputText v-if="botEditMode" v-model="notification.name"/>
          <div v-else>{{notification.name}}</div>
        </div>
      </template>

      <template #content>
        <div v-if="botEditMode">
          <div class="flex-auto pb-2">
            <label for="new-chat-id" class="font-bold block mb-2 pl-2">Новый токен:</label>
            <InputText type="password" v-model="newBotToken" class="w-full"/>
          </div>
          <div class="flex-auto pb-2">
            <label for="new-chat-id" class="font-bold block mb-2 pl-2">Описание:</label>
            <Textarea v-model="notification.description" rows="5" class="w-full"/>
          </div>
        </div>
        <p v-else>{{notification.description}}</p>
      </template>
    </Card>



    <Card style="max-width: 35rem!important; width: 100%">
      <template #title>
        <div class="flex flex-wrap justify-content-between gap-4">
          <div>Чаты <i class="pi pi-comments"/></div>
          <div><i class="pi pi-plus-circle cursor-pointer" @click="addNewMode=true"/></div>
        </div>
      </template>

      <template #content>

        <div v-if="addNewMode" class="pb-3 border-bottom-1 border-300 mb-3">
          <div class="flex flex-wrap flex-column gap-2 py-1">
            <div class="flex justify-content-between align-items-center gap-3">
              <p>Добавление нового чата</p>
              <ButtonGroup>
                <Button @click="addNewChat" icon="pi pi-check" severity="success"/>
                <Button @click="addNewMode=false" icon="pi pi-times"  severity="danger"/>
              </ButtonGroup>
            </div>

            <div class="flex-auto">
              <label for="new-chat-id" class="font-bold block mb-2">ID:</label>
              <InputText id="new-chat-id" style="font-family: monospace" v-model="newChat.id" class="w-full"/>
            </div>

            <div class="flex-auto">
              <label for="new-chat-name" class="font-bold block mb-2">Название:</label>
              <InputText id="new-chat-name" style="font-family: monospace" v-model="newChat.name" class="w-full"/>
            </div>

            <div class="flex-auto">
              <label for="new-chat-desc" class="font-bold block mb-2">Описание:</label>
              <InputText id="new-chat-desc" style="font-family: monospace" v-model="newChat.description" class="w-full"/>
            </div>
          </div>

        </div>

        <div v-for="c in notification.chats" @click="selectedChat=c" class="pb-3 mb-3 border-bottom-1 border-300">

          <div class="flex flex-wrap align-items-center gap-3 py-1 justify-content-between">
            <div class="flex flex-wrap gap-3 align-items-center">

              <i v-if="chatErrors.has(c.id)" v-tooltip.bottom="chatErrors.get(c.id)" class="pi pi-exclamation-circle text-2xl text-red-400"/>

              <div>
                <InputText v-if="isChatEdit(c)" v-model="c.name"/>
                <h3 v-else class="m-0 p-0">{{c.name}}</h3>
              </div>
              <div class="px-2 py-1 bg-primary-400 text-white border-round-md" style="font-family: monospace">ID: {{c.id}}</div>
            </div>

            <ButtonGroup>
              <Button @click="sendTestMessage(c)" size="small" v-tooltip.bottom="'Отправить тестовое сообщение'" icon="pi pi-send" severity="info"/>
              <Button v-if="isChatEdit(c)" @click="updateChat(c)" size="small" icon="pi pi-check" severity="success"/>
              <Button v-if="isChatEdit(c)" @click="chatEditMode=false" size="small" icon="pi pi-times" severity="warning"/>
              <Button v-else @click="editChat" icon="pi pi-pencil" size="small" outlined severity="warning"/>
              <Button @click="deleteChatDialogVisible=true" size="small" icon="pi pi-trash" outlined severity="danger"/>
            </ButtonGroup>
          </div>

          <div v-if="isChatEdit(c)">
            <Textarea v-model="c.description" class="w-full" rows="6"/>
          </div>
          <div v-else>
            {{c.description}}
          </div>
        </div>
      </template>
    </Card>

<!--    DELETE CHAT DIALOG-->
    <Dialog v-model:visible="deleteChatDialogVisible" class="pt-2" :show-header="false" modal :style="{ width: '25rem' }">
      <div class="flex align-items-center py-4">
        <i class="text-5xl pi pi-exclamation-circle mr-2 text-red-400"/>
        <h3 class="m-0 p-0">Вы уверены, что хотите удалить оповещение в чат?</h3>
      </div>

      <div v-if="selectedChat" class="flex flex-wrap align-items-center gap-3 justify-content-center">
        <h3>{{selectedChat.name}}</h3>
        <div class="px-2 py-1 bg-primary-400 text-white border-round-md" style="font-family: monospace">ID: {{selectedChat.id}}</div>
      </div>

      <div class="flex justify-content-end gap-2">
        <Button type="button" severity="primary" outlined autofocus label="Нет" @click="deleteChatDialogVisible = false"></Button>
        <Button type="button" severity="danger" outlined label="Удалить" @click="deleteChat"></Button>
      </div>
    </Dialog>

<!--    DELETE BOT DIALOG-->
    <Dialog v-model:visible="deleteBotDialogVisible" class="pt-2" :show-header="false" modal :style="{ width: '25rem' }">
      <div class="flex align-items-center py-4">
        <i class="text-5xl pi pi-exclamation-circle mr-2 text-red-400"/>
        <h3 class="m-0 p-0">Вы уверены, что хотите удалить бота оповещения?</h3>
      </div>

      <h3 class="m-0 mb-3 p-0 text-center">"{{notification.name}}"</h3>

      <div v-if="notification.chats.length > 0">
        <h4 class="text-center">Будут также удалены чаты:</h4>
        <div class="text-center">
          <div v-for="c in notification.chats" class="flex align-items-center justify-content-center gap-2 pb-2">
            <div>{{c.name}}</div>
            <div class="px-2 py-1 bg-primary-400 text-white border-round-md" style="font-family: monospace">ID: {{c.id}}</div>
          </div>
        </div>
      </div>

      <div class="flex justify-content-end gap-2">
        <Button type="button" severity="primary" outlined autofocus label="Нет" @click="deleteBotDialogVisible = false"></Button>
        <Button type="button" severity="danger" outlined label="Удалить" @click="deleteBot"></Button>
      </div>
    </Dialog>

  </div>

</template>

<script lang="ts">
import Textarea from "primevue/textarea";
import Badge from "primevue/badge/Badge.vue";
import {defineComponent, PropType} from 'vue'
import {TgNotification, Chat, TelegramNotificationsService} from "@/services/telegramNotifications";
import errorFmt from "@/errorFmt";


export default defineComponent({
  name: "TelegramNotification",
  components: {Badge, Textarea},
  props: {
    notification: {required: true, type: Object as PropType<TgNotification>},
    notificationService: {required: true, type: Object as PropType<TelegramNotificationsService>}
  },
  emits: ["update"],

  data() {
      return {
        originalNotificationName: this.notification.name,

        botEditMode: false,
        chatEditMode: false,
        addNewMode: false,
        newChat: {} as Chat,

        newBotToken: "",
        selectedChat: null as Chat|null,
        deleteChatDialogVisible: false,
        deleteBotDialogVisible: false,
        chatErrors: new Map() as Map<number,string>
      }
  },

  methods: {
    editChat() {
      this.chatEditMode = true
    },
    isChatEdit(chat: Chat) {
      return this.chatEditMode && chat == this.selectedChat
    },
    deleteChat() {
      if (this.selectedChat) {
        this.notificationService.deleteChat(this.originalNotificationName, this.selectedChat.id).then(
            () => {
              this.$emit("update");
              this.deleteChatDialogVisible = false;
            }
        )
      }
    },
    updateChat(chat: Chat) {
      this.notificationService.updateChat(this.originalNotificationName, chat).then(
          () => {
            this.chatEditMode = false;
            this.$emit("update");
          }
      )
    },
    addNewChat() {
      this.notificationService.addChat(this.originalNotificationName, this.newChat).then(
          () => {
            this.sendTestMessage(this.newChat)
            this.$emit("update");
            this.addNewMode = false;
            this.newChat = <Chat>{};
          }
      )
    },
    sendTestMessage(chat: Chat) {
      this.notificationService.sendTestMessage(this.originalNotificationName, chat.id).then(
          () => {
              this.$toast.add({
                severity: 'success',
                summary: 'Отправлено',
                detail: 'Проверьте чат',
                life: 5000
              });
              this.chatErrors.delete(chat.id)
          }
      ).catch(
          (error) => {
            const verboseError = errorFmt(error)
            console.log(verboseError)
            this.chatErrors.set(chat.id, verboseError)
          }
      )
    },


    updateBot() {
      this.notificationService.updateBot(
          this.originalNotificationName,
          this.notification.name,
          this.newBotToken,
          this.notification.description,
      ).then(
          () => {
            this.$emit("update")
            this.originalNotificationName = this.notification.name
            this.newBotToken = ""
            this.botEditMode = false
          }
      )
    },
    deleteBot() {
      this.notificationService.deleteBot(this.originalNotificationName).then(
          () => this.$emit("update")
      )
    },
  }
})
</script>

<style scoped>

</style>