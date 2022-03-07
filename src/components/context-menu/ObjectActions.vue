<script lang="ts">
import {
  computed,
  defineComponent,
} from 'vue';
import { useStore } from 'vuex';

export default defineComponent({
  props: {
    objKey: {
      type: String,
      required: false,
      default: null,
    },
  },
  emits: [
    'close',
  ],
  setup(props, { emit }) {
    const store = useStore();
    const userRating = computed(() => {
      return store.getters['rating/ratingByKey'](props.objKey);
    });
    const rate = async (value: number) => {
      const vote = {
        key: props.objKey,
        value,
      };
      await store.dispatch('rating/updateRating', vote);
      emit('close');
    };
    console.debug('props', props);
    const play = () => {
      console.debug('play', props.objKey);
      emit('close');
    };
    return {
      userRating,
      rate,
      play,
    };
  },
});
</script>

<template>
  <div
    class="actions"
  >
    <div
      class="action"
      @click.prevent="play"
    >
      <div
        class="action__icon"
      >
        [i]
      </div>
      <div
        class="action__name"
      >
        Als nächstes spielen
      </div>
    </div>
    <div
      class="action"
    >
      <div
        class="action__icon"
      >
        [i]
      </div>
      <div
        class="action__name"
      >
        Ans Ende der Warteschlange
      </div>
    </div>
    <div
      class="action"
      @click="rate(1)"
      v-if="(userRating && !userRating.value)"
    >
      <div
        class="action__icon"
      >
        [i]
      </div>
      <div
        class="action__name"
      >
        Zu meinen Favoriten
      </div>
    </div>
    <div
      class="action"
      @click="rate(null)"
      v-if="(userRating && userRating.value)"
    >
      <div
        class="action__icon"
      >
        [i]
      </div>
      <div
        class="action__name"
      >
        Aus Favoriten entfernen
      </div>
    </div>
    <div
      class="action"
      @click="rate(-1)"
    >
      <div
        class="action__icon"
      >
        [i]
      </div>
      <div
        class="action__name"
      >
        Mag ich nicht
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.actions {
  .action {
    display: flex;
    height: 3rem;
    align-items: center;
    border-bottom: 1px solid rgb(var(--c-gray-200));
    cursor: pointer;
    &:hover {
      background: rgb(var(--c-gray-100));
    }
    &__icon {
      height: 48px;
      width: 48px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    &__name {
      height: 48px;
      flex-grow: 1;
      padding-right: 1rem;
      display: flex;
      align-items: center;
      justify-content: flex-start;
    }
  }
}
</style>
