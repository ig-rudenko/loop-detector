import {Edge, Node} from "vis-network";
import {Data} from "vis-network/declarations/network/Network";


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

class GraphService {
    static getGraph(): GraphData {

        const nodes: Node[] = []
        const edges: EdgeData[] = []
        return {
            nodes,
            edges,
        }
    }
}

export {GraphService};
