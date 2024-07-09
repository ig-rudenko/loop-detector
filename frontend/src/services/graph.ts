import {Edge} from "vis-network";
import {Data} from "vis-network/declarations/network/Network";
import api from "@/services/api";
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
    private toast: ToastServiceMethods;

    constructor(toast: ToastServiceMethods) {
        this.toast = toast;
    }

    private toastError(error: any) {
        this.toast.add({
            severity: 'error',
            summary: 'Error',
            detail: getVerboseAxiosError(error),
            life: 5000
        });
    }

    async getCurrentGraph(depth: number = 1): Promise<GraphData> {
        try {
            const resp = await api.get<GraphData>("/graph/current?depth=" + depth);
            return resp.data;
        } catch (error: any) {
            this.toastError(error);
            return {nodes: [], edges: []};
        }
    }

    async getStoredGraphs(): Promise<StoredGraphFile[]> {
        try {
            const resp = await api.get<StoredGraphFile[]>("/graph/stored");
            return resp.data;

        } catch (error: any) {
            this.toastError(error);
            return [];
        }
    }

    async getStoredGraph(name: string): Promise<GraphData> {
        try {
            const resp = await api.get<GraphData>(`/graph/stored/${name}`);
            return resp.data;

        } catch (error: any) {
            this.toastError(error);
            return {nodes: [], edges: []};
        }
    }

    async deleteStoredGraph(name: string): Promise<void> {
        try {
            await api.delete(`/graph/stored/${name}`)
        } catch (error: any) {
            this.toastError(error);
        }
    }

}

export {GraphService};
