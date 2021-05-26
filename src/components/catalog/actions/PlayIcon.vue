<script lang="ts">
import IconPlay from '@/components/ui/icon/IconPlay.vue';

import { defineComponent, ref } from 'vue';
import { useStore } from 'vuex';
import { requireSubscription } from '@/utils/account';
import { getMedia } from '@/api/catalog';

export default defineComponent({
  components: {
    IconPlay,
  },
  props: {
    objKey: {
      type: String,
      required: true,
      default: null,
    },
  },
  setup(props) {
    const store = useStore();
    const isLoading = ref(false);
    const play = requireSubscription(async () => {
      isLoading.value = true;
      console.debug('play', props.objKey);
      const filter = {
        obj_key: props.objKey,
      };
      const { count, next, results } = await getMedia(20, 0, filter);
      console.debug('r', count, next, results);
      const payload = {
        mode: 'replace',
        media: results,
      };
      await store.dispatch('queue/updateQueue', payload);
      isLoading.value = false;
    });
    return {
      play,
      isLoading,
    };
  },
});
</script>

<template>
  <div
    class="play-icon"
  >
    <div
      @click="play"
      class="container"
      :class="{'is-loading': isLoading}"
    >
      <IconPlay
        :size="40"
        color="rgb(var(--c-white))"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.play-icon {
  .container {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    background: rgba(var(--c-black), 0.6);
    border: 1px solid rgba(var(--c-white), 0.5);
    border-radius: 24px;
    cursor: pointer;
    transition: background 100ms;
    &:hover {
      background: rgba(var(--c-black), 0.9);
    }
  }
}
</style>
