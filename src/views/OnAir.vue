<script lang="ts">
import { computed } from 'vue';
import { useStore } from 'vuex';

import ScheduleItem from '@/components/broadcast/onair/ScheduleItem.vue';

export default {
  components: {
    ScheduleItem,
  },
  setup() {
    const store = useStore();
    const current = computed(() => store.getters['schedule/current']);
    const next = computed(() => store.getters['schedule/next']);
    const past = computed(() => store.getters['schedule/past']);
    return {
      current,
      next,
      past,
    };
  },
};
</script>

<template>
  <div class="on-air">
    (( On Air ))
    <div
      class="schedule"
    >
      <ScheduleItem
        v-if="next"
        :schedule-item="next"
      />
      <ScheduleItem
        v-if="current"
        :schedule-item="current"
        :is-current="true"
      />
      <ScheduleItem
        v-for="item in past"
        :key="item.key"
        :schedule-item="item"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.schedule {
  display: grid;
  //grid-template-columns: repeat( auto-fit, minmax(250px, 1fr) );
  //grid-template-columns: repeat( auto-fill, minmax(250px, 1fr) );
  grid-template-columns: repeat( 1000, minmax(250px, 1fr) );
  overflow-x: scroll;
  grid-gap: 1rem;
}
</style>
