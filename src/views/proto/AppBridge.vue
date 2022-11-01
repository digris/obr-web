<script lang="ts">
import { computed, defineComponent } from "vue";
import { storeToRefs } from "pinia";
import { useQueueState } from "@/composables/queue";
import { usePlayerControls } from "@/composables/player";
import { usePlayerStore } from "@/stores/player";

export default defineComponent({
  components: {},
  setup() {
    const { queuedMedia: media } = useQueueState();
    const mediaUids = computed(() => {
      return media.value.map((m: any) => m?.uid);
    });
    const { appPlayerData } = storeToRefs(usePlayerStore());
    const { playLive, pause, resume } = usePlayerControls();
    return {
      media,
      mediaUids,
      appPlayerData,
      //
      playLive,
      pause,
      resume,
    };
  },
});
</script>
<template>
  <div class="app-bridge">
    <h2>APP Bridge</h2>
    <section>
      <h4>store: queue/mediaUids</h4>
      <pre v-text="mediaUids" />
      <h4>store: player/appPlayerData</h4>
      <pre v-text="appPlayerData" />
    </section>
    <section>
      <h4>Controls</h4>
      <button @click.prevent="playLive">Play Live</button>
      <button>Pause</button>
    </section>
  </div>
</template>
<style lang="scss" scoped>
@use "@/style/elements/section";
@use "@/style/elements/button";

.app-bridge {
  padding: 1rem;
  > section {
    @include section.default;
  }
  button {
    @include button.default;
    cursor: pointer;
  }
}
</style>
