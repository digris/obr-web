<script lang="ts">
import { defineComponent } from "vue";
import { useI18n } from "vue-i18n";

import { getMedia } from "@/api/catalog";
import IconEnueue from "@/components/ui/icon/IconEnqueue.vue";
import { useAnalytics } from "@/composables/analytics";
import { useQueueControls } from "@/composables/queue";
import { requireSubscription } from "@/utils/account";

import Action from "./actions/Action.vue";

export default defineComponent({
  props: {
    filter: {
      type: Object,
      required: false,
      default: () => ({}),
    },
    ordering: {
      type: Array,
      default: () => [],
    },
  },
  components: {
    Action,
    IconEnueue,
  },
  emits: ["close"],
  setup(props, { emit }) {
    const { t } = useI18n();
    const { logUIEvent } = useAnalytics();
    const iconScale = 0.875;
    const { enqueueMedia, startPlayCurrent } = useQueueControls();
    const enqueue = async (mode: string) => {
      const filter = { ...props.filter };
      const ordering = props.ordering;
      const { results } = await getMedia(100, 0, filter, ordering);
      await enqueueMedia(results, mode);
    };
    const enqueueNext = requireSubscription(async () => {
      await enqueue("insert");
      emit("close");
      logUIEvent("player:enqueue-next", "list");
    });
    const enqueueEnd = requireSubscription(async () => {
      await enqueue("append");
      await startPlayCurrent();
      emit("close");
      logUIEvent("player:enqueue-end", "list");
    });
    return {
      t,
      iconScale,
      enqueueNext,
      enqueueEnd,
    };
  },
});
</script>

<template>
  <div class="actions">
    <section>
      <Action @click="enqueueNext" :label="t('player.enqueueNext')">
        <template #icon>
          <IconEnueue :scale="iconScale" />
        </template>
      </Action>
      <Action @click="enqueueEnd" :label="t('player.enqueueEnd')">
        <template #icon>
          <IconEnueue :scale="iconScale" :flip-y="true" />
        </template>
      </Action>
    </section>
  </div>
</template>
