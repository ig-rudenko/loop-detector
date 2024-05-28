<template>
  <div>
    <Button :label="showGraph?'Скрыть график':'Показать график'" class="my-2" :outlined="showGraph"
            :icon="showGraph?'pi pi-window-minimize':'pi pi-chart-bar'"
            @click="showGraph = !showGraph"/>
    <div v-show="showGraph">
      <!--      График-->
      <div id="graph-vis"></div>

      <!--      Легенда-->
      <div v-if="graph2d" class="flex flex-wrap">
        <div v-for="group in groups" class="p-2 flex align-items-center gap-1">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" :fill="stringToColour(String(group.title))"
               viewBox="0 0 16 16"><circle cx="8" cy="8" r="8"></circle></svg>
          <span>{{ group.title }}</span>
        </div>
      </div>
    </div>
  </div>

  <div v-if="selected.show" :style="{left: `${selected.x}px`, top: `${selected.y}px`, 'z-index': 99999}" class="p-2 absolute p-card">
    IP: {{selected.group}}
  </div>

</template>

<script lang="ts">
import {defineComponent, PropType} from "vue";
import {DataGroup, Graph2d, Graph2dOptions} from "vis-timeline";
import "vis-timeline/styles/vis-timeline-graph2d.min.css"


export default defineComponent({
  name: "MessagesChart",
  props: {
    data: {required: true, type: Object as PropType<any[]>},
  },

  data() {
    return {
      groups: [] as DataGroup[],
      colorsIPsMap: new Map() as Map<string, string>,
      graphData: [] as any[],
      showGraph: true,
      graph2d: null as Graph2d | null,

      selected: {
        show: false,
        group: "",
        x: 0,
        y: 0,
      }
    }
  },

  mounted() {
    let container: HTMLElement = document.getElementById('graph-vis')!;

    let uniqueIPs: string[] = []
    let minTime: Date = new Date(this.data[0]["@timestamp"])
    let maxTime: Date = new Date(this.data[0]["@timestamp"])

    const datesMap: Map<string, number> = new Map()

    this.data.forEach((item: any) => {
      const hostIp = item["host"]["ip"]

      if (uniqueIPs.indexOf(hostIp) === -1) uniqueIPs.push(hostIp);

      const time: Date = new Date(item["@timestamp"])

      if (time < minTime) minTime = time;
      if (time > maxTime) maxTime = time;

      const timeString = time.toLocaleDateString() + " " + time.toLocaleTimeString().slice(0, -2);
      const mapKey = timeString + "|" + hostIp;

      let dateCount = datesMap.get(mapKey);
      if (dateCount) {
        datesMap.set(mapKey, dateCount + 1)
      } else {
        datesMap.set(mapKey, 1);
      }
    });


    for (const [key, value] of datesMap.entries()) {
      const [dateStr, hostIp] = key.split("|");

      this.graphData.push(
          {
            x: this.parseDateTime(dateStr + ":00"),
            y: value,
            group: hostIp,
            label: hostIp,
          }
      )
    }

    for (let i = 0; i < uniqueIPs.length; i++) {
      const ip = uniqueIPs[i]
      const groupColor = this.stringToColour(ip)
      this.colorsIPsMap.set(groupColor, ip)
      this.groups.push({
        id: ip,
        content: ip,
        title: ip,
        style: `stroke: ${groupColor}; fill: ${groupColor}`,
      })
    }

    let options: Graph2dOptions = {
      style: 'bar',
      drawPoints: false,
      stack: true,
      legend: false,
      start: minTime,
      end: maxTime,
      sort: true,
      showCurrentTime: true,
      showMinorLabels: true,
    };

    this.graph2d = new Graph2d(container, this.graphData, this.groups, options)
    this.graph2d.on(
        "click",
        (action: any) => {
          console.log(action.event.target.getBoundingClientRect());
          if (action.event.changedPointers?.length) {
            const colorMatch = String(action.event.changedPointers[0].srcElement.attributes.style.value).match(/#\S{6}/);
            if (colorMatch) {
              const elementRect = action.event.target.getBoundingClientRect()
              this.selected.show = true;
              this.selected.group = this.colorsIPsMap.get(colorMatch[0]) || "";
              this.selected.x = elementRect.x;
              this.selected.y = elementRect.y - 50;
              return
            }
          }
          this.selected.show = false;
        }
    )
  },

  methods: {
    parseDateTime(dateTimeString: string): Date {
      // Разбиваем строку на дату и время
      const [datePart, timePart] = dateTimeString.split(' ');

      // Разбиваем часть даты
      const [day, month, year] = datePart.split('.').map(Number);

      // Разбиваем часть времени
      const [hours, minutes, seconds] = timePart.split(':').map(Number);

      // Создаем объект Date
      return new Date(year, month - 1, day, hours, minutes, seconds);
    },
    stringToColour(str: string): string {
      if (!str) return '';
      str = str + str;
      let hash = 0;
      for (let i = 0; i < str.length; i++) {
        hash = str.toLowerCase().charCodeAt(i) + ((hash << 4) - hash);
      }
      let c = (hash & 0x00FFFFFF).toString(16).toUpperCase();
      return "#" + "00000".substring(0, 6 - c.length) + c;
    },
  }
})

</script>

<style scoped>

</style>