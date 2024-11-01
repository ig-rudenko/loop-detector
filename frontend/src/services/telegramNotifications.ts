import {AxiosResponse} from "axios";

import api from "@/services/api";
import getVerboseAxiosError from "@/errorFmt";
import {errorToast, successToast} from "@/services/my.toast";


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

    async addBot(name: string, token: string, description: string): Promise<void> {
        try {
            await api.post("/notifications/telegram", {
                name: name,
                token: token,
                description: description,
            })
        } catch (error: any) {
            errorToast('Ошибка создания бота', getVerboseAxiosError(error))
            throw error
        }
    }

    async updateBot(notificationName: string, newName?: string, newToken?: string, newDescription?: string): Promise<void> {
        let updateData: any = {}
        if (newName != undefined && newName.length > 0) updateData["name"] = newName
        if (newToken != undefined && newToken.length > 0) updateData["token"] = newToken
        if (newDescription != undefined && newDescription.length > 0) updateData["description"] = newDescription

        try {
            await api.patch("/notifications/telegram/" + notificationName, updateData)
        } catch (error: any) {
            errorToast('ошибка обновления бота', getVerboseAxiosError(error))
            throw error
        }
    }

    async deleteBot(notificationName: string): Promise<void> {
        try {
            await api.delete("/notifications/telegram/" + notificationName)
        } catch (error: any) {
            errorToast('Ошибка удаления бота', getVerboseAxiosError(error))
            throw error
        }
    }


    // CHATS

    async getNotifications(): Promise<TgNotification[]> {
        try {
            const response: AxiosResponse<TgNotification[]> = await api.get('/notifications/telegram');
            return response.data;
        } catch (error: any) {
            errorToast('Ошибка получения списка оповещений', getVerboseAxiosError(error))
            throw error
        }
    }

    async addChat(notificationName: string, chat: Chat): Promise<AxiosResponse<any, any>> {
        try {
            return await api.post(
                "/notifications/telegram/" + notificationName + "/chats",
                chat
            )
        } catch (error: any) {
            errorToast('Ошибка добавления чата к боту', getVerboseAxiosError(error))
            throw error
        }
    }

    async updateChat(notificationName: string, chat: Chat): Promise<void> {
        try {
            await api.patch(
                "/notifications/telegram/" + notificationName + "/chats/" + chat.id,
                chat
            )
        } catch (error: any) {
            errorToast('Ошибка обновления чата бота', getVerboseAxiosError(error))
            throw error
        }
    }

    async deleteChat(notificationName: string, chatID: number): Promise<void> {
        try {
            await api.delete("/notifications/telegram/" + notificationName + "/chats/" + chatID)
        } catch (error: any) {
            errorToast('Ошибка удаления чата бота', getVerboseAxiosError(error))
            throw error
        }
    }

    async sendTestMessage(notificationName: string, chatID: number): Promise<AxiosResponse<any, any>> {
        const url = "/notifications/telegram/" + notificationName + "/chats/" + chatID + "/testMessage"
        try {
            const resp = await api.post(url);
            successToast('Тестовое сообщение отправлено', "Проверьте чат", 5000);
            return resp;
        } catch (error: any) {
            errorToast('Ошибка отправки тестового сообщения', getVerboseAxiosError(error));
            throw error;
        }
    }

}

const telegramNotificationService = new TelegramNotificationsService();
export default telegramNotificationService;