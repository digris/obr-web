<script lang="ts">
import { computed, defineComponent } from "vue";
import { useI18n } from "vue-i18n";
import { useShare } from "@vueuse/core";
import { debounce } from "lodash-es";

import IconEnueue from "@/components/ui/icon/IconEnqueue.vue";
import IconFlash from "@/components/ui/icon/IconFlash.vue";
import IconHeart from "@/components/ui/icon/IconHeart.vue";
import IconShare from "@/components/ui/icon/IconShare.vue";
import { useObjKey } from "@/composables/obj";
import { useQueueControls } from "@/composables/queue";
import { useRating } from "@/composables/rating";
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
    IconShare,
  },
  emits: ["close"],
  setup(props, { emit }) {
    const { t } = useI18n();
    const { objKey } = useObjKey(props.obj);
    const iconScale = 0.875;
    const { ratingByKey, setRatingWithSource } = useRating();
    const rating = computed(() => ratingByKey(objKey.value));
    const isFavorite = computed(() => rating.value === 1);
    const isBanned = computed(() => rating.value === -1);
    const rate = debounce(
      async (value: number) => {
        await setRatingWithSource(objKey.value, value);
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
    const { share, isSupported: shareSupported } = useShare();
    const shareObj = () => {
      const title = props.obj?.name ?? document.title;
      const url = props.obj?.detailUrl ?? document.location.href;
      share({
        title,
        url,
      });
      emit("close");
    };
    return {
      t,
      iconScale,
      isFavorite,
      isBanned,
      canBan,
      rate,
      enqueueNext,
      enqueueEnd,
      shareSupported,
      shareObj,
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
    <section v-if="shareSupported">
      <Action @click="shareObj()" :label="t('player.share')">
        <template #icon>
          <IconShare :scale="iconScale" />
        </template>
      </Action>
    </section>
  </div>
</template>
