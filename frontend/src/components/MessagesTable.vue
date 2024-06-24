<template>
  <DataTable :value="messages" size="small" data-key="timestamp"
             v-model:filters="filters" :globalFilterFields="['message']"
             paginator :rows="10" paginator-position="top" :always-show-paginator="false" removableSort>

    <template #header>
      <div><h3 v-html="header"></h3></div>
      <div>Всего сообщений: {{messages.length}}</div>
      <div class="mt-3 flex align-items-center flex-wrap justify-content-between">
          <div><Button type="button" icon="pi pi-filter-slash" label="Clear" size="small" outlined @click="clearFilter()" /></div>
          <IconField iconPosition="left">
            <InputIcon><i class="pi pi-search" /></InputIcon>
            <InputText size="small" v-model="filters['global'].value" placeholder="Keyword Search" />
          </IconField>
      </div>
    </template>
    <template #empty>Нет логов</template>

    <Column field="timestamp" header="@timestamp" :sortable="true" class="table-font"></Column>
    <Column field="message" header="Message" class="table-font">
      <template #body="{data}">
        <div v-html="formatWithMarkMessage(data['message'])"></div>
      </template>
    </Column>
  </DataTable>
</template>

<script lang="ts">
import {defineComponent, PropType} from "vue";
import {FilterMatchMode} from "primevue/api";
import {formatMessage, formatMessageWithMark} from "@/services/messages.formatter.ts";
import {Message} from "@/services/graph";

export default defineComponent({
  name: "MessagesTable",
  props: {
    messages: {required: true, type: Object as PropType<Message[]>},
    header: {required: true, type: String},
  },

  data() {
      return {
        filters: {
          global: { value: null, matchMode: FilterMatchMode.CONTAINS },
        }
      }
  },
  methods: {
    clearFilter() {
      this.filters.global.value = null;
    },
    formatWithMarkMessage(message: string) {
      if (this.filters.global.value) {
        return formatMessageWithMark(message, this.filters.global.value);
      }
      return formatMessage(message);
    },
  }
});

</script>

<style>
.table-font {
  font-family: "Lucida Console",monospace;
  font-size: 0.9rem;
}
</style>