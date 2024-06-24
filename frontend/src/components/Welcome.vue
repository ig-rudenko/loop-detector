<template>

  <div class="grid grid-nogutter bg-white-alpha-40 text-800 border-round mt-4">
    <div class="col-12 md:col-6 p-4 text-center md:text-left flex align-items-center ">
      <section class="section-margin">
        <span class="block text-6xl font-bold mb-1">Ecstasy Loop</span>
        <div class="text-6xl text-primary font-bold mb-3">визуализация петель</div>
        <p class="mt-0 mb-4 text-700 text-xl line-height-3">
          Приложение предназначено для анализа и мониторинга сетевых петель.
          <br>
          Оно помогает выявлять и визуализировать текущие петли на сети, а также просматривать историю их возникновения.
          <br>
          Приложение обрабатывает логи, поступающие от сетевого оборудования, и определяет наличие петель в реальном
          времени. При обнаружении петли, приложение предоставляет графическое отображение связей между устройствами,
          что позволяет легко локализовать проблему и определить, на каком оборудовании её искать.
        </p>
      </section>
    </div>
    <div class="col-12 md:col-6 overflow-hidden border-round">
      <img src="/img/welcome-graph.gif" alt="Image" class="md:ml-auto block md:h-full welcome-image">
    </div>
  </div>

  <div class="flex justify-content-center my-5">
    <div class="mb-3 font-bold text-3xl">
      <span class="text-900">Принцип работы</span>
    </div>
  </div>

  <div>
    <Timeline :value="events" align="alternate" class="customized-timeline">
      <template #marker="slotProps">
        <span
            class="flex w-2rem h-2rem align-items-center justify-content-center text-white border-circle z-1 shadow-1"
            :style="{ backgroundColor: slotProps.item.color }">
            <i :class="slotProps.item.icon"></i>
        </span>
      </template>
      <template #content="slotProps">
        <div :class="slotProps.item.classes">
          <Card class="mt-3 w-fit shadow-2">
            <template #title>{{ slotProps.item.status }}</template>
            <template #content>
              <img v-if="slotProps.item.image" :src="slotProps.item.image" :alt="slotProps.item.name"
                   :width="slotProps.item.width"/>
              <p v-html="slotProps.item.text"></p>
            </template>
          </Card>
        </div>
      </template>
    </Timeline>
  </div>
</template>

<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "Welcome",
  data() {
    return {
      events: [
        {
          status: 'Формирование логов',
          icon: 'pi pi-chart-bar',
          color: '#fcc416',
          width: 420,
          image: '/img/logs-to-es.svg',
          classes: ['flex', 'justify-content-start'],
          text: "Сетевое оборудование отправляет логи на Elasticsearch.",
        },
        {
          status: 'Анализ логов',
          icon: 'pi pi-file',
          color: '#d72a22',
          image: '/img/analyze-logs.svg',
          width: 550,
          classes: ['flex', 'justify-content-end'],
          text: "Периодически просматриваем логи в поисках упоминания петель<br> и записываем в Redis",
        },
        {
          status: 'Формирование графа',
          icon: 'pi pi-share-alt',
          color: '#6900fd',
          width: 550,
          image: '/img/logs-to-graph.svg',
          classes: ['flex', 'justify-content-start'],
          text: "На основе логов формируем граф связей",
        },
      ]
    };
  }
})
</script>

<style scoped>
.welcome-image {
  clip-path: polygon(15% 0, 100% 0%, 100% 100%, 0 100%);
}
.section-margin {
  margin-left: 1rem;
}
</style>

<style lang="scss" scoped>
@media screen and (max-width: 767px) {
  ::v-deep(.customized-timeline) {
    .p-timeline-event:nth-child(even) {
      flex-direction: row;

      .p-timeline-event-content {
        text-align: left;
      }
    }

    .p-timeline-event-opposite {
      flex: 0;
      display: none;
    }

    .p-timeline-event-separator {
      display: none;
    }
  }

  img {
    max-width: 100% !important;
  }

  .welcome-image {
    clip-path: none;
  }

  .section-margin {
    margin-left: 0;
  }
}
</style>