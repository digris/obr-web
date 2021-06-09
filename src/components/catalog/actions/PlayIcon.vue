<script lang="ts">
import IconPlay from '@/components/ui/icon/IconPlay.vue';

import { defineComponent, ref } from 'vue';
import { useStore } from 'vuex';
import { requireSubscription } from '@/utils/account';
import { getMedia } from '@/api/catalog';
import eventBus from '@/eventBus';

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
      const filter = {
        obj_key: props.objKey,
      };
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
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  display: flex;
  align-items: center;
  justify-content: center;
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
    &.is-loading {
      cursor: wait;
      opacity: 0.8;
    }
  }
}
</style>
