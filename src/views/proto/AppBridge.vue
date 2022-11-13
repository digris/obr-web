<script lang="ts">
import { computed, defineComponent, ref } from "vue";
import { storeToRefs } from "pinia";
import { useQueueState } from "@/composables/queue";
import { usePlayerControls } from "@/composables/player";
import { usePlayerStore } from "@/stores/player";

export default defineComponent({
  components: {},
  setup() {
    const appBridge = window.appBridge;
    const { queuedMedia: media } = useQueueState();
    const mediaUids = computed(() => {
      return media.value.map((m: any) => m?.uid);
    });
    const { appPlayerData } = storeToRefs(usePlayerStore());
    const { playLive, pause, resume } = usePlayerControls();
    const channel = ref("");
    const data = ref("");
    const sendData = async () => {
      // @ts-ignore
      await appBridge.send(channel.value, data.value ? data.value : null);
    };
    return {
      media,
      mediaUids,
      appPlayerData,
      //
      playLive,
      pause,
      resume,
      sendData,
      channel,
      data,
    };
  },
});
</script>
<template>
  <div class="app-bridge">
    <h2>APP Bridge</h2>
    <section>
      <h4>Controls</h4>
      <button @click.prevent="playLive">Play Live</button>
      <button @click.prevent="pause">Pause</button>
      <button @click.prevent="resume">Resume</button>
    </section>
    <section>
      <h4>Send to Swift</h4>
      <form @submit.prevent="sendData">
        <div>
          <h6>channel</h6>
          <input v-model="channel" />
        </div>
        <div>
          <h6>data</h6>
          <textarea v-model="data"></textarea>
        </div>
        <div>
          <button>Send</button>
        </div>
      </form>
    </section>
    <section>
      <h4>store: player/appPlayerData</h4>
      <pre v-text="appPlayerData" />
      <h4>store: queue/mediaUids</h4>
      <pre v-text="mediaUids" />
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
    @include button.default(2rem);
    cursor: pointer;
  }
  form {
    > div {
      margin-bottom: 1rem;
      display: flex;
      flex-direction: column;
      align-items: start;
      justify-content: start;
      > input,
      > textarea {
        font-family: monospace;
        padding: 4px 8px;
        width: 100%;
      }
      > textarea {
        min-height: 80px;
      }
    }
  }
}
</style>
