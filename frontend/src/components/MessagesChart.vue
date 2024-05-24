<template>
  <div>
    <Button :label="showGraph?'Скрыть график':'Показать график'" class="my-2" :outlined="showGraph"
            :icon="showGraph?'pi pi-window-minimize':'pi pi-chart-bar'"
    @click="showGraph = !showGraph"/>
    <div v-show="showGraph" id="graph-vis"></div>
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
      graphData: [] as any[],
      showGraph: true,
    }
  },

  mounted() {
    let container: HTMLElement = document.getElementById('graph-vis')!;
    let groups: DataGroup[] = [];

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
      groups.push({id: uniqueIPs[i], content: uniqueIPs[i], title: uniqueIPs[i]})
    }

    let options: Graph2dOptions = {
      style: 'bar',
      drawPoints: false,
      stack: true,
      legend: true,
      start: minTime,
      end: maxTime,
      sort: true,
      showCurrentTime: true,
      showMinorLabels: true,
    };

    const graph2d = new Graph2d(container, this.graphData, groups, options)
    console.log(graph2d)
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
    }
  }
})

</script>

<style scoped>

</style>