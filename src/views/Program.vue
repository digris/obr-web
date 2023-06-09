<script lang="ts" setup>
/*
 * NOTE: the naming here is kind of confusing and maybe should be changed.
 * this view (views/Program.view) is used as top-level view bound to /program/
 * the actual program data is handled by components/broadcast/program/Program.vue
 */
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import type { DateTime } from "luxon";

import Program from "@/components/broadcast/program/Program.vue";

defineProps<{
  date: DateTime;
}>();

const { t } = useI18n();
const router = useRouter();
const onDateUpdate = (date: DateTime) => {
  router.push({
    name: "program",
    params: {
      date: date.toISODate(),
    },
  });
};
</script>

<template>
  <div class="program-view">
    <Program :title="t('menu.program')" :date="date" @date-update="onDateUpdate" />
  </div>
</template>

<style lang="scss" scoped>
.program-view {
  flex-grow: 1;
}
</style>
