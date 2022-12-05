<script lang="ts">
import { debounce } from "lodash-es";
import { computed, defineComponent } from "vue";
import { useI18n } from "vue-i18n";

import IconEnueue from "@/components/ui/icon/IconEnqueue.vue";
import IconFlash from "@/components/ui/icon/IconFlash.vue";
import IconHeart from "@/components/ui/icon/IconHeart.vue";
import { useObjKey } from "@/composables/obj";
import { useQueueControls } from "@/composables/queue";
import { useRatingStore } from "@/stores/rating";
import { requireSubscription } from "@/utils/account";

import Action from "./actions/Action.vue";

export default defineComponent({
  props: {
    obj: {
      type: Object,
      required: true,
      default: () => {},
    },
  },
  components: {
    Action,
    IconEnueue,
    IconHeart,
    IconFlash,
  },
  emits: ["close"],
  setup(props, { emit }) {
    const { t } = useI18n();
    const { objKey } = useObjKey(props.obj);
    const iconScale = 0.875;
    const { ratingByKey, setRating } = useRatingStore();
    const rating = computed(() => ratingByKey(objKey.value));
    const isFavorite = computed(() => rating.value === 1);
    const isBanned = computed(() => rating.value === -1);
    const rate = debounce(
      async (value: number) => {
        await setRating(objKey.value, value);
      },
      200,
      { leading: true, trailing: false }
    );
    const canBan = computed(() => {
      return props.obj?.ct && props.obj.ct === "catalog.media";
    });
    const { enqueueObj, startPlayCurrent } = useQueueControls();
    const enqueueNext = requireSubscription(async () => {
      await enqueueObj(props.obj, "insert");
      await startPlayCurrent();
      emit("close");
    });
    const enqueueEnd = requireSubscription(async () => {
      await enqueueObj(props.obj, "append");
      await startPlayCurrent();
      emit("close");
    });
    return {
      t,
      iconScale,
      isFavorite,
      isBanned,
      canBan,
      rate,
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
    <section>
      <Action v-if="!isFavorite" @click="rate(1)" :label="t('player.favoritesAdd')">
        <template #icon>
          <IconHeart :scale="iconScale" :outlined="true" />
        </template>
      </Action>
      <Action v-else @click="rate(null)" :label="t('player.favoritesRemove')">
        <template #icon>
          <IconHeart :scale="iconScale" />
        </template>
      </Action>
    </section>
    <section v-if="canBan">
      <Action v-if="!isBanned" @click="rate(-1)" :label="t('player.bannedAdd')">
        <template #icon>
          <IconFlash :scale="iconScale" :outlined="true" />
        </template>
      </Action>
      <Action v-else @click="rate(0)" :label="t('player.bannedRemove')">
        <template #icon>
          <IconFlash :scale="iconScale" />
        </template>
      </Action>
    </section>
  </div>
</template>
