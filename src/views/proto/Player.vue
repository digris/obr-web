<script lang="ts">
import { defineComponent } from "vue";
import { usePlayerControls } from "@/composables/player";
import shaka from "shaka-player";

const SHAKA_CONFIG = {
  manifest: {
    dash: {
      ignoreMinBufferTime: true,
    },
  },
  abr: {
    switchInterval: 2,
    defaultBandwidthEstimate: 1000000, // 10 Mbit/s
    bandwidthDowngradeTarget: 0.4,
    bandwidthUpgradeTarget: 0.2,
    // NOTE: testing bw limitations
    // restrictions: {
    //   maxBandwidth: 512000,
    // },
  },
  streaming: {
    bufferingGoal: 30,
    rebufferingGoal: 0.1,
    bufferBehind: 0.1,
    retryParameters: {
      maxAttempts: 100,
    },
    useNativeHlsOnSafari: false,
  },
};

export default defineComponent({
  components: {},
  setup() {
    const { pause, resume } = usePlayerControls();
    const audioPlayer = window.audioPlayer;

    // shaka
    const audio = document.createElement("audio");
    const player = new shaka.Player(audio);

    window.a = audio;
    window.p = player;

    player.configure(SHAKA_CONFIG);

    const playLive = async () => {
      const url = `https://stream-abr.next.openbroadcast.ch/hls/manifest.m3u8?1669637128310`;
      console.debug("playOnDemand", url);
      try {
        await player.load(url);
        // This runs if the asynchronous load is successful.
        console.log("player - audio loaded");
        try {
          await audio.play();
          console.log("audio - play started");
        } catch (e) {
          console.error("audio error", e);
        }
      } catch (e) {
        // onError is executed if the asynchronous load fails.
        console.error("player error", e);
      }
    };

    const unblockPlay = async () => {
      // audio.src = "https://stream.next.openbroadcast.ch/256.mp3"
      audio.src =
        "data:audio/wav;base64,UklGRsgAAABXQVZFZm10ICgAAAD+/wIAgD4AAAD0AQAIACAAFgAgAAMAAAABAAAAAAAQAIAAAKoAOJtxZmFjdAQAAAAQAAAAZGF0YYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==";
      await audio.play();
    };

    const playOnDemand = async () => {
      await unblockPlay();
      // const uid = "E323524B";
      const uid = "59044F07";
      const url = `http://local.obr-next:5000/encoded/${uid}/hls/manifest.m3u8`;
      // const url = `https://media.next.openbroadcast.ch/encoded/1A43C245/hls/manifest.m3u8`
      console.debug("playOnDemand", url);
      try {
        await player.load(url);
        // This runs if the asynchronous load is successful.
        console.log("player - audio loaded");
        try {
          await audio.play();
          console.log("audio - play started");
        } catch (e) {
          console.error("audio error", e);
        }
      } catch (e) {
        // onError is executed if the asynchronous load fails.
        console.error("player error", e);
      }
    };
    // const playOnDemand = () => {
    //   const uid = "E323524B";
    //   const url = `http://local.obr-next:5000/encoded/${uid}/hls/manifest.m3u8`
    //   console.debug('playOnDemand', url);
    //   audioPlayer.play(url);
    // };

    const shakaPlayOnDemand = async (uid) => {
      // const uid = "59044F07";
      const url = `http://local.obr-next:5000/encoded/${uid}/hls/manifest.m3u8`;
      await audioPlayer.play(url);
    };

    const shakaPlayLive = async () => {
      const url = `https://stream-abr.next.openbroadcast.ch/hls/manifest.m3u8?1669637128310`;
      await audioPlayer.play(url);
    };

    return {
      playLive,
      playOnDemand,
      pause,
      resume,
      unblockPlay,
      //
      shakaPlayOnDemand,
      shakaPlayLive,
    };
  },
});
</script>
<template>
  <div class="player-dev">
    <h2>Player (Shaka)</h2>
    <section>
      <h4>Controls</h4>
      <div class="controls">
        <button @click.prevent="shakaPlayLive">Live</button>
        <button @click.prevent="shakaPlayOnDemand('59044F07')">OD 59044F07</button>
        <button @click.prevent="shakaPlayOnDemand('317F268D')">OD 317F268D</button>
      </div>
    </section>
  </div>
  <!--
  <div class="player-dev">
    <h2>Player</h2>
    <section>
      <h4>Controls</h4>
      <div class="controls">
        <button @click.prevent="playLive">Live</button>
        <button @click.prevent="playOnDemand">On Demanbd</button>
        <button @click.prevent="pause">Pause</button>
        <button @click.prevent="resume">Resume</button>
        <button @click.prevent="unblockPlay">unblock</button>
      </div>
    </section>
  </div>
  -->
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

  .controls {
    display: flex;
  }
}
</style>
