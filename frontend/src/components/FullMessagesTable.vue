<template>
  <DataTable :value="messages" size="small" data-key="@timestamp"
             v-model:filters="filters" :globalFilterFields="['message']"
             paginator :rows="10" paginator-position="top" :always-show-paginator="false" removableSort>

    <template #header>
      <div>Всего: {{ messages.length }}</div>
      <div class="mt-3 flex align-items-center flex-wrap justify-content-between">
        <div>
          <Button type="button" icon="pi pi-filter-slash" label="Clear" size="small" outlined @click="clearFilter()"/>
        </div>
        <IconField iconPosition="left">
          <InputIcon><i class="pi pi-search"/></InputIcon>
          <InputText size="small" v-model="filters['global'].value" placeholder="Keyword Search"/>
        </IconField>
      </div>
    </template>
    <template #empty>Нет логов</template>

    <Column field="@timestamp" header="@timestamp" :sortable="true" class="table-font">
      <template #body="{data}">
        {{ getVerboseDate(data['@timestamp']) }}
      </template>
    </Column>
    <Column field="host.ip" header="IP" :sortable="true" class="table-font"></Column>
    <Column field="message" header="Message" class="table-font"></Column>
  </DataTable>
</template>

<script lang="ts">
import {defineComponent, PropType} from 'vue'
import {FilterMatchMode} from "primevue/api";
import {DetailMessage} from "@/types.ts";


export default defineComponent({
  name: "FullMessagesTable",
  props: {
    messages: {required: true, type: Object as PropType<DetailMessage[]>},
  },

  data() {
    return {
      filters: {
        global: {value: null, matchMode: FilterMatchMode.CONTAINS},
      }
    }
  },
  methods: {
    clearFilter() {
      this.filters.global.value = null;
    },
    getVerboseDate(dateStr: string) {
      console.log(dateStr)
      const date = new Date(dateStr);
      return date.toLocaleDateString() + " " + date.toLocaleTimeString() + "." + date.getMilliseconds();
    }
  }
})
</script>

<style scoped>

</style>