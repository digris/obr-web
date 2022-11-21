<script lang="ts">
import { computed, defineComponent, ref } from "vue";
import { storeToRefs } from "pinia";
import { usePlayerState } from "@/composables/player";
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
    const {
      state: playerState,
      mode: playerMode,
      absPosition: playerAbsPosition,
    } = usePlayerState();
    const { appPlayerData } = storeToRefs(usePlayerStore());
    const { playLive, pause, resume } = usePlayerControls();
    const channel = ref("");
    const data = ref("");
    const sendData = async () => {
      console.debug("data", data.value);
      // @ts-ignore
      await appBridge.send(channel.value, data.value ? JSON.parse(data.value) : null);
    };
    const socialBegin = () => {
      window.appBridge?.send("browser:navigate", {
        url: "https://europe-west6-open-broadcast.cloudfunctions.net/social-auth-redirector",
      });
    };
    return {
      media,
      mediaUids,
      appPlayerData,
      //
      playerMode,
      playerState,
      playerAbsPosition,
      //
      playLive,
      pause,
      resume,
      sendData,
      channel,
      data,
      socialBegin,
    };
  },
});
</script>
<template>
  <div class="app-bridge">
    <h2>APP Bridge</h2>
    <section>
      <h4>Controls</h4>
      <div class="controls">
        <button @click.prevent="playLive">Play Live</button>
        <button @click.prevent="pause">Pause</button>
        <button @click.prevent="resume">Resume</button>
      </div>
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
      <h4>player</h4>
      <pre
        v-text="{
          mode: playerMode,
          state: playerState,
          absPosition: playerAbsPosition,
        }"
      />
      <h4>queue/mediaUids</h4>
      <pre v-text="mediaUids" />
    </section>
    <section class="app-links">
      <!--
      <a
        rel="noopener noreferrer"
        href="https://next.openbroadcast.ch/proto/app-bridge/"
        class="button"
      >App Link</a>
      <a
        rel="noopener noreferrer"
        target="_blank"
        href="https://next.openbroadcast.ch/proto/app-bridge/"
        class="button"
      >App Link (target: blank)</a>
      <a
        rel="noopener noreferrer"
        target="_blank"
        href="obrapp://next.openbroadcast.ch/proto/app-bridge/"
        class="button"
      >App Link (obrapp://)</a>
      <a
        rel="noopener noreferrer"
        href="http://local.next.openbroadcast.ch:3000/dev/redirect/"
        class="button"
      >App Link (redirect via local domain)</a>
      -->
      <a
        rel="noopener noreferrer"
        href="https://europe-west6-open-broadcast.cloudfunctions.net/social-auth-redirector"
        class="button"
      >Login via redirect</a>
      <a @click.prevent="socialBegin" class="button">System qbrowser via redirect</a>
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
    margin-bottom: 4rem;
  }
  button,
  .button {
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
  .controls {
    display: flex;
  }
  .app-links {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style>
