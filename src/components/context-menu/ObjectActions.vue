<script lang="ts">
import { computed, defineComponent } from "vue";
import { useI18n } from "vue-i18n";

import { useObjKey } from "@/composables/obj";
import { requireSubscription } from "@/utils/account";
import { useObjRating } from "@/composables/rating";
import { useQueueControls } from "@/composables/queue";

import IconEnueue from "@/components/ui/icon/IconEnqueue.vue";
import IconHeart from "@/components/ui/icon/IconHeart.vue";
import IconFlash from "@/components/ui/icon/IconFlash.vue";
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
    const iconSize = 42;
    const iconColor = "rgb(var(--c-black))";
    const { userRating, isFavorite, isBanned, rate } = useObjRating(objKey.value);
    const canBan = computed(() => {
      return props.obj?.ct && props.obj.ct === "catalog.media";
    });
    const {
      // enqueueMedia,
      enqueueObj,
      startPlayCurrent,
    } = useQueueControls();
    const enqueueNext = requireSubscription(async () => {
      // enqueueMedia([props.obj], 'insert');
      await enqueueObj(props.obj, "insert");
      await startPlayCurrent();
      emit("close");
    });
    const enqueueEnd = requireSubscription(async () => {
      // enqueueMedia([props.obj], 'append');
      await enqueueObj(props.obj, "append");
      await startPlayCurrent();
      emit("close");
    });
    return {
      t,
      iconSize,
      iconColor,
      //
      userRating,
      isFavorite,
      isBanned,
      canBan,
      rate,
      //
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
          <IconEnueue :size="iconSize" :color="iconColor" />
        </template>
      </Action>
      <Action @click="enqueueEnd" :label="t('player.enqueueEnd')">
        <template #icon>
          <IconEnueue :size="iconSize" :color="iconColor" :flip-y="true" />
        </template>
      </Action>
    </section>
    <section>
      <Action v-if="!isFavorite" @click="rate(1)" :label="t('player.favoritesAdd')">
        <template #icon>
          <IconHeart :size="iconSize" :color="iconColor" :outlined="true" />
        </template>
      </Action>
      <Action v-else @click="rate(null)" :label="t('player.favoritesRemove')">
        <template #icon>
          <IconHeart :size="iconSize" :color="iconColor" />
        </template>
      </Action>
    </section>
    <section v-if="canBan">
      <Action v-if="!isBanned" @click="rate(-1)" :label="t('player.bannedAdd')">
        <template #icon>
          <IconFlash :size="iconSize" :color="iconColor" :outlined="true" />
        </template>
      </Action>
      <Action v-else @click="rate(0)" :label="t('player.bannedRemove')">
        <template #icon>
          <IconFlash :size="iconSize" :color="iconColor" />
        </template>
      </Action>
    </section>
  </div>
</template>
