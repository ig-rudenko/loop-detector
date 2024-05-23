import {Edge} from "vis-network";
import {Data} from "vis-network/declarations/network/Network";
import api from "@/services/api";
import {useToast} from "primevue/usetoast";
import getVerboseAxiosError from "@/errorFmt.ts";
import {ToastServiceMethods} from "primevue/toastservice";


export interface Message {
    timestamp: string;
    message: string;
}

export interface EdgeData extends Edge {
    messages: Message[];
}

export interface GraphData extends Data {
    edges?: EdgeData[];
}


export interface StoredGraphFile {
    name: string;
    modTime: string;
}


class GraphService {

    private static toastError(toast: ToastServiceMethods, error: any) {
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: getVerboseAxiosError(error),
            life: 5000
        });
    }

    static async getCurrentGraph(): Promise<GraphData> {
        const toast = useToast();
        try {
            const resp = await api.get<GraphData>("/graph/current");
            return resp.data;

        } catch (error: any) {
            this.toastError(toast, error);
            return {nodes: [], edges: []};
        }
    }

    static async getStoredGraphs(): Promise<StoredGraphFile[]>{
        const toast = useToast();
        try {
            const resp = await api.get<StoredGraphFile[]>("/graph/stored");
            return resp.data;

        } catch (error: any) {
            this.toastError(toast, error);
            return [];
        }
    }

    static async getStoredGraph(name: string): Promise<GraphData> {
        const toast = useToast();
        try {
            const resp = await api.get<GraphData>(`/graph/stored/${name}`);
            return resp.data;

        } catch (error: any) {
            this.toastError(toast, error);
            return {nodes: [], edges: []};
        }
    }

}

export {GraphService};
