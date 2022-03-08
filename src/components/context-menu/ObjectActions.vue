<script lang="ts">
import {
  computed,
  // computed,
  defineComponent,
} from 'vue';

import { requireSubscription } from '@/utils/account';
import { useObjRating } from '@/composables/rating';
import { useQueueControls } from '@/composables/queue';

import IconEnueue from '@/components/ui/icon/IconEnueue.vue';
import IconHeart from '@/components/ui/icon/IconHeart.vue';
import IconFlash from '@/components/ui/icon/IconFlash.vue';

export default defineComponent({
  props: {
    obj: {
      type: Object,
      required: true,
      default: () => {},
    },
  },
  components: {
    IconEnueue,
    IconHeart,
    IconFlash,
  },
  emits: [
    'close',
  ],
  setup(props, { emit }) {
    // const store = useStore();
    // const userRating = computed(() => {
    //   return store.getters['rating/ratingByKey'](props.objKey);
    // });
    // const rate = async (value: number) => {
    //   const vote = {
    //     key: props.objKey,
    //     value,
    //   };
    //   await store.dispatch('rating/updateRating', vote);
    //   emit('close');
    // };
    const objKey = computed(() => `${props.obj.ct}:${props.obj.uid}`);
    const iconSize = 42;
    const iconColor = 'rgb(var(--c-black))';
    const {
      userRating,
      isFavorite,
      isBanned,
      rate,
    } = useObjRating(objKey.value);
    const {
      enqueueMedia,
      startPlayCurrent,
    } = useQueueControls();
    const enqueueNext = requireSubscription(() => {
      enqueueMedia([props.obj], 'insert');
      startPlayCurrent();
      emit('close');
    }, 'foo');
    const enqueueEnd = requireSubscription(() => {
      enqueueMedia([props.obj], 'append');
      startPlayCurrent();
      emit('close');
    }, 'foo');
    return {
      iconSize,
      iconColor,
      //
      userRating,
      isFavorite,
      isBanned,
      rate,
      //
      enqueueNext,
      enqueueEnd,
    };
  },
});
</script>

<template>
  <div
    class="actions"
  >
    <section>
      <div
        class="action"
        @click.prevent="enqueueNext"
      >
        <div
          class="action__icon"
        >
          <IconEnueue
            :size="iconSize"
            :color="iconColor"
          />
        </div>
        <div
          class="action__name"
        >
          Als nächstes spielen
        </div>
      </div>
      <div
        class="action"
        @click.prevent="enqueueEnd"
      >
        <div
          class="action__icon"
        >
          <IconEnueue
            :size="iconSize"
            :color="iconColor"
            :flip-y="true"
          />
        </div>
        <div
          class="action__name"
        >
          Ans Ende der Warteschlange
        </div>
      </div>
    </section>
    <section>
      <div
        v-if="!isFavorite"
        @click="rate(1)"
        class="action"
      >
        <div
          class="action__icon"
        >
          <IconHeart
            :size="iconSize"
            :color="iconColor"
            :outlined="true"
          />
        </div>
        <div
          class="action__name"
        >
          Zu meinen Favoriten
        </div>
      </div>
      <div
        v-else
        class="action"
        @click="rate(null)"
      >
        <div
          class="action__icon"
        >
          <IconHeart
            :size="iconSize"
            :color="iconColor"
          />
        </div>
        <div
          class="action__name"
        >
          Aus Favoriten entfernen
        </div>
      </div>
    </section>
    <section>
      <div
        v-if="!isBanned"
        @click="rate(-1)"
        class="action"
      >
        <div
          class="action__icon"
        >
          <IconFlash
            :size="iconSize"
            :color="iconColor"
            :outlined="true"
          />
        </div>
        <div
          class="action__name"
        >
          Mag ich nicht
        </div>
      </div>
      <div
        v-else
        class="action"
        @click="rate(null)"
      >
        <div
          class="action__icon"
        >
          <IconFlash
            :size="iconSize"
            :color="iconColor"
          />
        </div>
        <div
          class="action__name"
        >
          Mag ich doch
        </div>
      </div>
    </section>
  </div>
</template>

<style lang="scss" scoped>
.actions {
  .action {
    display: flex;
    align-items: center;
    height: 3rem;
    border-bottom: 1px solid rgb(var(--c-gray-200));
    cursor: pointer;
    &:hover {
      background: rgb(var(--c-gray-100));
    }
    &__icon {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 48px;
      height: 48px;
    }
    &__name {
      display: flex;
      flex-grow: 1;
      align-items: center;
      justify-content: flex-start;
      height: 48px;
      padding-right: 1rem;
    }
  }
}
</style>
