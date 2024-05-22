<template>
  <Splitter style="height:800px">
    <SplitterPanel class="flex align-items-center justify-content-center">
      <div id="net" style="height: 800px; width: 100%"></div>
    </SplitterPanel>

    <SplitterPanel style="overflow: auto" :size="35">
      <p v-if="selectedNode">Node ID: {{ selectedNode }}</p>

      <MessagesTable v-if="selectedEdge"
                     :messages="selectedEdge.messages" :header="String(selectedEdge.id)"/>
    </SplitterPanel>

  </Splitter>

</template>

<script lang="ts">
import 'vis-network/styles/vis-network.min.css';

import {defineComponent} from "vue";
import {Network} from "vis-network";
import {Options} from "vis-network/declarations/network/Network";
import GraphImage from "@/components/GraphImage.vue";
import {EdgeData, GraphData, GraphService, Message} from "@/services/graph";
import MessagesTable from "@/components/MessagesTable.vue";

export default defineComponent({
  name: "Graph",
  components: {MessagesTable, GraphImage},
  data() {
    return {
      network: null as Network | null,
      nodes: new Map(),
      edges: new Map(),

      selectedNode: null as Node | null,
      selectedEdge: null as EdgeData|null,
      visibleSidebar: false,
    }
  },
  mounted() {
    let container: HTMLElement = document.getElementById('net')!;
    let data: GraphData = GraphService.getGraph();

    data.nodes!.forEach(item => {
      item.title = this.htmlTitle((<string>item.title));
      this.nodes.set(item.id, item);
    });

    data.edges!.forEach((item: EdgeData) => {
      item.title = this.htmlTitle((<string>item.title));
      this.formatMessages(item.messages);
      this.edges.set(item.id, item)
    });

    this.selectedEdge = (<EdgeData[]>data.edges!)[0]

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

    this.network = new Network(container, data, options);
    this.network.on("click", this.onNetworkClick);
  },

  methods: {
    htmlTitle(html: string): HTMLElement {
      const container = document.createElement("div");
      container.innerHTML = html;
      return container;
    },

    onNetworkClick(params: any) {
      if (params.edges.length > 0 && params.nodes.length === 0) {
        this.selectedEdge = this.edges.get(params.edges[0])
        this.selectedNode = null
      }
      if (params.nodes.length > 0) {
        this.selectedNode = params.nodes[0];
        this.selectedEdge = null;
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
