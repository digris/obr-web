<script lang="ts">
import { defineComponent } from "vue";
import { usePlayerState } from "@/composables/player";

export default defineComponent({
  components: {},
  setup() {
    const { media } = usePlayerState();
    return {
      media,
    };
  },
});
</script>

<template>
  <div v-if="media" class="player">
    (( MOBILE PLAYER ))
  </div>
</template>

<style lang="scss" scoped>
.player {
  position: fixed;
  bottom: 0;
  z-index: 110;
  width: 100%;
  color: rgba(var(--c-fg));
  background: rgba(var(--c-bg));
}
</style>
