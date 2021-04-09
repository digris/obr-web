<script lang="ts">
import CircleButton from '@/components/UI/button/CircleButton.vue';
import IconPlay from '@/components/UI/icon/IconPlay.vue';

import { defineComponent, ref } from 'vue';

export default defineComponent({
  components: {
    CircleButton,
    IconPlay,
  },
  setup() {
    const state = ref('stopped');
    const click = (e: Event) => {
      console.debug('click', e);
    };
    return {
      state,
      click,
    };
  },
});
</script>

<template>
  <div
    @click="click"
    class="player-control-icon"
    :class="`is-${state}`"
  >
    <CircleButton
      :size="24"
    >
      <IconPlay
        :size="20"
      />
    </CircleButton>
  </div>
</template>

<style lang="scss" scoped>
.player-control-icon {
  display: flex;
  align-items: center;
}
</style>
