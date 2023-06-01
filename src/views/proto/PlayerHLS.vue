<script lang="ts" setup>
import { onMounted, ref } from "vue";
// import Hls from "hls.js/dist/hls.light.js";
import Hls from "hls.js";

// console.debug("Hls", Hls);

const playLive = async () => {
  console.debug("play live");
  const url = "https://obr-stream-hls.hazelfire.com/live.m3u8";
  await hls.loadSource(url);
  el.value.play();
};

const playOnDemand = async (uid: string) => {
  console.debug("play on-demand", uid);
  const url = `https://media.next.openbroadcast.ch/encoded/${uid}/hls/manifest.m3u8`;
  // const url = `http://local.obr-next:3000/encoded/${uid}/hls/manifest.m3u8`;
  await hls.loadSource(url);
  el.value.play();
};

const hls = new Hls({
  debug: true,
  maxBufferLength: 30,
  maxMaxBufferLength: 30,
  backBufferLength: 30,
  liveDurationInfinity: true,
  //
  xhrSetup: (xhr, url) => {
    console.debug(url, xhr);
    xhr.withCredentials = true;
  },
});

hls.on(Hls.Events.MEDIA_ATTACHED, function () {
  console.debug("audio and hls.js are now bound together !");
});

hls.on(Hls.Events.MANIFEST_PARSED, function (event, data) {
  console.debug(event, data.levels);
});

hls.on(Hls.Events.ERROR, function (event, data) {
  console.debug(event, data.levels);
});

const el = ref(null);

onMounted(() => {
  console.debug("mounted -> init player");

  hls.attachMedia(el.value);

  window.hls = hls;
  window.audioEl = el.value;
});
</script>
<template>
  <div class="player-dev">
    <h2>Player (HLS)</h2>
    <section>
      <div>
        <audio ref="el" controls />
      </div>
      <h4>Controls</h4>
      <div class="controls">
        <button @click.prevent="playLive">Live</button>
        <button @click.prevent="playOnDemand('EA0E6C02')">OD EA0E6C02</button>
        <button @click.prevent="playOnDemand('317F268D')">OD 317F268D</button>
      </div>
    </section>
  </div>
</template>
<style lang="scss" scoped>
@use "@/style/elements/section";
@use "@/style/elements/button";

.player-dev {
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
