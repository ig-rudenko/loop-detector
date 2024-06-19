import api from "@/services/api.ts";
import {useToast} from "primevue/usetoast";
import getVerboseAxiosError from "@/errorFmt.ts";
import {ToastServiceMethods} from "primevue/toastservice";
import {de} from "vis-network/declarations/network/locales";


export interface Chat {
    id: number
    name: string
    description: string
}

export interface TgNotification {
    name: string
    description: string
    chats: Chat[]
}

export class TelegramNotificationsService {
    private toast: ToastServiceMethods;

    constructor() {
        this.toast = useToast()
    }

    private toastError(error: any) {
        this.toast.add({
            severity: 'error',
            summary: 'Error',
            detail: getVerboseAxiosError(error),
            life: 7000
        });
    }

    async addBot(name: string, token: string, description: string) {
        try {
            await api.post("/notifications/telegram", {
                name: name,
                token: token,
                description: description,
            })
        } catch (error) {
            this.toastError(error)
            throw error
        }
    }

    async updateBot(notificationName: string, newName?: string, newToken?: string, newDescription?: string) {
        let updateData: any = {}
        if (newName != undefined && newName.length > 0) updateData["name"] = newName
        if (newToken != undefined && newToken.length > 0) updateData["token"] = newToken
        if (newDescription != undefined && newDescription.length > 0) updateData["description"] = newDescription

        try {
            await api.patch("/notifications/telegram/" + notificationName, updateData)
        } catch (error) {
            this.toastError(error)
            throw error
        }
    }

    async deleteBot(notificationName: string) {
        try {
            await api.delete("/notifications/telegram/" + notificationName)
        } catch (error) {
            this.toastError(error)
            throw error
        }
    }


    // CHATS

    async getNotifications() {
        try {
            const response = await api.get<TgNotification[]>('/notifications/telegram');
            return response.data;
        } catch (error) {
            this.toastError(error);
            throw error
        }
    }

    async addChat(notificationName: string, chat: Chat) {
        try {
            const resp = await api.post(
                "/notifications/telegram/" + notificationName + "/chats",
                chat
            )
            return resp
        } catch (error) {
            this.toastError(error)
            throw error
        }
    }

    async updateChat(notificationName: string, chat: Chat) {
        try {
            await api.patch(
                "/notifications/telegram/" + notificationName + "/chats/" + chat.id,
                chat
            )
        } catch (error) {
            this.toastError(error)
            throw error
        }
    }

    async deleteChat(notificationName: string, chatID: number) {
        try {
            await api.delete("/notifications/telegram/" + notificationName + "/chats/" + chatID)
        } catch (error) {
            this.toastError(error)
            throw error
        }
    }

    async sendTestMessage(notificationName: string, chatID: number) {
        try {
            return await api.post("/notifications/telegram/" + notificationName + "/chats/" + chatID + "/testMessage")
        } catch (error) {
            this.toastError(error)
            throw error
        }
    }

}