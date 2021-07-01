<script lang="ts">
import { defineComponent, ref } from 'vue';
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
      };
      // NOTE: hm - this is not very nice...
      await store.dispatch('queue/updateQueue', payload);
      eventBus.emit('queue:controls:startPlayCurrent');
      isLoading.value = false;
    }, 'Subscription required.');
    return {
      play,
      isLoading,
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
      :class="{'is-loading': isLoading}"
    >
      <slot name="default">
        Play
      </slot>
    </div>
  </div>
</template>
