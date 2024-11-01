import {Edge} from "vis-network";
import {Data} from "vis-network/declarations/network/Network";

import api from "@/services/api";
import errorFmt from "@/errorFmt";
import {errorToast} from "@/services/my.toast";


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

interface GraphInfo {
    messagesCount: number
    vlans: { vid: number, count: number }[]
}

export interface StoredGraph {
    name: string;
    modTime: string;
}

export interface StoredGraphInfo extends StoredGraph {
    info: GraphInfo
}

export interface PaginatedStoredGraphInfo {
    count: number
    results: StoredGraphInfo[]
}

class GraphService {
    private graphsInfo: Map<string, GraphInfo> = new Map<string, GraphInfo>();

    async getCurrentGraph(depth: number = 1): Promise<GraphData> {
        try {
            const resp = await api.get<GraphData>("/graph/current?depth=" + depth);
            return resp.data;
        } catch (error: any) {
            errorToast("Ошибка загрузки графа", errorFmt(error))
            return {nodes: [], edges: []};
        }
    }

    async getStoredGraph(name: string): Promise<GraphData> {
        try {
            const resp = await api.get<GraphData>(`/graph/stored/${name}`);
            return resp.data;

        } catch (error: any) {
            errorToast("Ошибка загрузки графа", errorFmt(error))
            return {nodes: [], edges: []};
        }
    }

    async getStoredGraphInfo(name: string): Promise<GraphInfo|null> {
        const graph = this.graphsInfo.get(name);
        if (graph) return graph;

        try {
            const resp = await api.get<GraphInfo>("/graph-info/" + name);
            this.graphsInfo.set(name, resp.data);
            return resp.data;
        } catch (error: any) {
            errorToast("Ошибка загрузки графа", errorFmt(error))
            return null;
        }
    }

    async getStoredGraphsInfoPage(page: number, perPage: number): Promise<PaginatedStoredGraphInfo|null> {
        const url = `/graph/stored?page=${page}&size=${perPage}`
        try {
            const resp = await api.get<PaginatedStoredGraphInfo>(url);
            return resp.data;
        } catch (error: any) {
            errorToast("Ошибка загрузки графа", errorFmt(error))
            return null;
        }
    }

    async getGraphsHistory(): Promise<StoredGraph[]> {
        try {
            const resp = await api.get<StoredGraph[]>("/graph/history");
            return resp.data;
        } catch (error: any) {
            errorToast("Ошибка загрузки истории графа", errorFmt(error))
            return [];
        }
    }

    async deleteStoredGraph(name: string): Promise<void> {
        try {
            await api.delete(`/graph/stored/${name}`)
        } catch (error: any) {
            errorToast("Ошибка удаления истории графа", errorFmt(error))
        }
    }

}

export const graphService = new GraphService();
