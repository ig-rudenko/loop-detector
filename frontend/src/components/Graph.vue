<template>
  <Splitter v-if="graphData.nodes?.length" style="height:800px">
    <SplitterPanel class="flex align-items-center justify-content-center">
      <div id="net" style="height: 800px; width: 100%"></div>
    </SplitterPanel>

    <SplitterPanel style="overflow: auto" :size="35">
      <div>
        <MessagesTable v-if="selected.messages.length"
                       :messages="selected.messages" :header="selectedMessagesHeader"/>
        <div v-else class="p-3">
          <h3 v-html="selectedMessagesHeader"></h3>
          Нет сообщений
        </div>
      </div>
    </SplitterPanel>

  </Splitter>

  <!--EMPTY-->
  <div v-else class="flex justify-content-center">
    <div>
      <h1 class="text-center">Нет петель на сети!</h1>
    </div>
  </div>

</template>

<script lang="ts">
import 'vis-network/styles/vis-network.min.css';

import {defineComponent, PropType} from "vue";
import {Network} from "vis-network";
import {Options, Node} from "vis-network/declarations/network/Network";
import GraphImage from "@/components/GraphImage.vue";
import {EdgeData, GraphData, Message} from "@/services/graph";
import MessagesTable from "@/components/MessagesTable.vue";

export default defineComponent({
  name: "Graph",
  components: {MessagesTable, GraphImage},
  props: {
    graphData: {required: true, type: Object as PropType<GraphData>}
  },
  data() {
    return {
      network: null as Network | null,
      nodes: new Map(),
      edges: new Map(),

      selected: {
        node: null as Node | null,
        edges: [] as EdgeData[],
        messages: [] as Message[],
      },
      visibleSidebar: false,
    }
  },
  mounted() {
    if (!this.graphData.nodes?.length) return;

    let container: HTMLElement = document.getElementById('net')!;

    // NODES
    this.graphData.nodes!.forEach(item => {
      item.title = this.htmlTitle((<string>item.title));
      this.nodes.set(item.id, item);
    });

    // EDGE
    this.graphData.edges!.forEach((item: EdgeData) => {
      item.title = this.htmlTitle(this.getEdgeTitle(<string>item.title));
      this.formatMessages(item.messages);
      this.edges.set(item.id, item)
    });

    if (this.graphData.edges?.length) {
      // Начальное отображение сообщений
      this.selected.messages = (<EdgeData[]>this.graphData.edges)[0].messages
      this.selected.edges = [(<EdgeData[]>this.graphData.edges)[0]]
    }

    let options: Options = {
      interaction: {
        hideEdgesOnDrag: false, hideNodesOnDrag: false, dragNodes: true
      },
      configure: {
        enabled: false
      },
      physics: {
        enabled: true, solver: 'repulsion'
      },
      edges: {
        arrows: {middle: true},
        smooth: true, color: {inherit: true}
      }
    };

    this.network = new Network(container, this.graphData, options);
    this.network.on("click", this.onNetworkClick);
  },

  computed: {

    selectedMessagesHeader(): string {
      if (this.selected.node) {
        return String((<HTMLElement>this.selected.node.title).innerHTML);
      }

      if (this.selected.edges.length > 0) {
        let [fromDevice, toDevice] = String(this.selected.edges[0]!.id).split(":::")
        const edgeLabelElement = <HTMLElement>this.selected.edges[0].title
        const mathPorts = edgeLabelElement.innerHTML.match(/>(.*?) -&gt; (.*?)<br>/)

        let fromPort, toPort = ""
        if (mathPorts) {
          fromPort = mathPorts[1]
          toPort = mathPorts[2]
        }
        return `Линк от '${fromDevice}' (${fromPort}) до '${toDevice}' (${toPort})`
      }
      return ""
    },
  },

  methods: {

    getEdgeTitle(title: string): string {
      return `<h3>${title}</h3>`
    },

    htmlTitle(html: string): HTMLElement {
      const container = document.createElement("div");
      container.innerHTML = html;
      return container;
    },

    onNetworkClick(params: any) {
      // EDGES SELECT
      if (params.edges.length > 0 && params.nodes.length === 0) {
        this.selected.node = null
        this.selected.edges = [this.edges.get(params.edges[0])]
        this.setSelectedMessagesForEdges(params.edges)
      }

      // NODES
      if (params.nodes.length > 0) {
        this.selected.node = this.nodes.get(params.nodes[0]);
        this.selected.edges = [];
        for (const edgeId of params.edges) {
          this.selected.edges.push(this.edges.get(edgeId));
        }
        this.setSelectedMessagesForEdges(params.edges)
      }
    },

    setSelectedMessagesForEdges(edges: EdgeData[]) {
      this.selected.messages = []
      for (const edgeID of edges) {
        this.selected.messages.push(...this.edges.get(edgeID).messages)
      }
    },

    formatMessages(messages: Message[]) {
      messages.forEach(item => {
        const date = new Date(item.timestamp);
        item.timestamp = date.toLocaleDateString() + " " + date.toLocaleTimeString() + "." + date.getMilliseconds();
      })
    }
  }
})
</script>

<style scoped>
</style>
