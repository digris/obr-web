<script lang="ts">
import { computed, defineComponent } from 'vue';
import { useStore } from 'vuex';

export default defineComponent({
  setup() {
    const store = useStore();
    const playerState = computed(() => store.getters['player/playerState']);

    return {
      data: {
        state: playerState,
      },
    };
  },
});
</script>

<template>
  <div
    class="stream-info"
  >
    <pre
      v-text="data"
    />
  </div>
</template>

<style lang="scss" scoped>
.stream-info {
  position: fixed;
  bottom: 76px;
  left: 4px;
  background: black;
  padding: 0.5rem;
  color: white;
  font-size: 13px;
}
</style>
