import {AxiosError} from "axios";

import api from "@/services/api";
import {DetailMessage} from "@/types";
import getVerboseAxiosError from "@/errorFmt";
import {errorToast, successToast} from "@/services/my.toast";

class MessagesService {
    async getCurrentMessages(): Promise<DetailMessage[]> {
        try {
            const resp = await api.get<DetailMessage[]>("/messages/")
            return resp.data;
        } catch (error: any) {
            errorToast('Ошибка получения сообщений', getVerboseAxiosError(error));
            return []
        }
    }

    async getGraphMessages(graphName: string): Promise<DetailMessage[]> {
        try {
            const resp = await api.get<DetailMessage[]>("/messages/stored/" + graphName)
            return resp.data;
        } catch (error: any) {
            errorToast('Ошибка получения сообщений', getVerboseAxiosError(error));
            return []
        }
    }

    deleteCurrentMessages() {
        api.delete("/messages/")
            .then(() => successToast('Удалено', "Все сообщения были удалены"))
            .catch((error: AxiosError) => errorToast('Ошибка удаления сообщений', getVerboseAxiosError(error)))
    }
}


const messagesService = new MessagesService();
export default messagesService;