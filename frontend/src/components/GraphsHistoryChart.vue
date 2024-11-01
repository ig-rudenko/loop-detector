<template>
  <div id="graph-vis"></div>

  <OverlayPanel ref="graphHistoryLoopPanel">
    <LoopPreviewCard v-if="selectedLoop" :graph-data="selectedLoop" />
  </OverlayPanel>

</template>

<script lang="ts">
import {defineComponent, PropType} from "vue";
import {DataItem, Timeline} from "vis-timeline";
import "vis-timeline/styles/vis-timeline-graph2d.min.css"
import {graphService, StoredGraphInfo} from "@/services/graph";
import LoopPreviewCard from "@/components/LoopPreviewCard.vue";
import OverlayPanel from "primevue/overlaypanel";

export interface HistoryItem {
  datetime: string;
  name: string;
}

export default defineComponent({
  name: "GraphsHistoryChart",
  components: {LoopPreviewCard},
  props: {
    data: {required: true, type: Object as PropType<HistoryItem[]>},
  },

  data() {
    return {
      graphData: [] as DataItem[],
      timeline: null as Timeline | null,
      selectedLoop: null as StoredGraphInfo | null,
    }
  },

  mounted() {
    let container: HTMLElement = document.getElementById('graph-vis')!;

    for (let i = 0; i < this.data.length; i++) {
      this.graphData.push(
          {
            id: i,
            content: this.data[i].name,
            start: this.data[i].datetime,
          }
      )
    }

    const options = {
      height: 400,
      locale: "ru_RU",
    }

    this.timeline = new Timeline(container, this.graphData, options)
    this.timeline.on(
        "click",
        (action: any) => {
          if (action.what == "item") {
            const loopName = action.event.target.innerText;
            graphService.getStoredGraphInfo(loopName).then(
                value => {
                  if (!value) return;
                  this.selectedLoop = {
                    name: loopName,
                    modTime: action.time,
                    info: value
                  };
                  (<OverlayPanel>this.$refs.graphHistoryLoopPanel).toggle(action.event, action.event.target)
                }
            )
          }
        }
    )
  },

})

</script>
