<script lang="ts">
import { computed, defineComponent, ref } from 'vue';
import { useStore } from 'vuex';
import { requireSubscription } from '@/utils/account';
import { getMedia } from '@/api/catalog';
import eventBus from '@/eventBus';

export default defineComponent({
  props: {
    objKey: {
      type: String,
      required: false,
      default: null,
    },
    filter: {
      type: Object,
      required: false,
      default: () => {},
    },
  },
  setup(props) {
    const store = useStore();
    const isLoading = ref(false);
    const playerScope = computed(() => store.getters['player/currentScope']);
    const inScope = computed(() => {
      return playerScope.value.includes(props.objKey);
    });
    const play = requireSubscription(async () => {
      isLoading.value = true;
      const filter = { ...props.filter };
      if (props.objKey) {
        filter.obj_key = props.objKey;
      }
      const { results } = await getMedia(100, 0, filter);
      const payload = {
        mode: 'replace',
        media: results,
        scope: (props.objKey) ? [props.objKey] : null,
      };
      eventBus.emit('queue:controls:enqueue', payload);
      isLoading.value = false;
    }, 'Subscription required.');
    return {
      play,
      isLoading,
      inScope,
    };
  },
});
</script>

<template>
  <div
    class="play-action"
  >
    <div
      @click="play"
      class="container"
      :class="{
        'is-loading': isLoading,
        'in-scope': inScope,
      }"
    >
      <slot
        name="default"
        :isLoading="isLoading"
      >
        Play
      </slot>
    </div>
  </div>
</template>
