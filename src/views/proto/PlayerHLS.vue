<script lang="ts" setup>
import { computed, onMounted, ref } from "vue";
import { useRafFn } from "@vueuse/core";
import { round } from "lodash-es";

import { getMedia } from "@/api/catalog";
import { useAnalyser, usePlayerControls, usePlayerState } from "@/composables/player";
import { useQueueControls } from "@/composables/queue";
import type { AnnotatedMedia } from "@/stores/queue";

const {
  mode,
  playState,
  duration,
  currentTime,
  relPosition,
  liveLatency,
  bandwidth,
  media,
  scope,
  color,
  debugData,
} = usePlayerState();

const { playLive, playMedia, pause, resume, seek } = usePlayerControls();

const { enqueueMedia, startPlayCurrent } = useQueueControls();

// const queue = ref([]);
const queue = ref<Array<AnnotatedMedia>>([]);
const loadPlaylist = async (uid: string) => {
  const { results } = await getMedia(
    100,
    0,
    {
      obj_key: `catalog.playlist:${uid}`,
    },
    []
  );
  console.debug(results);
  queue.value = results;

  await enqueueMedia(results, "replace");
  await startPlayCurrent(true);
};

const { analyser } = useAnalyser();

const spectrum = ref(new Uint8Array(16));

// analyser
// useRafFn(() => {
//   const a = analyser?.a32;
//   const sd = new Uint8Array(16);
//   if (a) {
//     a.getByteFrequencyData(sd);
//   }
//   // spectrum.value = sd.slice(12, 72);
//   spectrum.value = sd;
// });

const spectrum4 = computed(() => {
  const sd = spectrum.value;
  const sd4 = [sd[4] * 0.8, sd[6], sd[8], sd[10]];
  return sd4.map((d) => Math.min(round((d / 255) * 150, 1), 100));
});

const canvas = ref();
const ctx = ref<CanvasRenderingContext2D>();
onMounted(() => {
  ctx.value = canvas.value.getContext("2d");
});

const draw = (drawData: Array<number>) => {
  const c = ctx.value;
  if (!c) {
    return;
  }
  c.clearRect(0, 0, canvas.value.width, canvas.value.height);
  for (let i = 0; i < drawData.length; i++) {
    const x = i * 6;
    const h = (drawData[i] / 100) * 21;
    const y = 21 - h;
    c.beginPath();
    c.fillStyle = "blue";
    c.fillRect(x, y, 3, h);
    c.fill();
  }
};

const a = analyser?.a32;

const { pause: pauseDraw, resume: resumeDraw } = useRafFn(() => {
  if (!a) {
    return;
  }
  const sd = new Uint8Array(16);
  a.getByteFrequencyData(sd);
  const sd4 = [sd[4] * 0.8, sd[6], sd[8], sd[10] * 1.2];
  const drawData = sd4.map((d) => Math.min(round((d / 255) * 170, 1), 100));
  draw(drawData);
});
</script>

<template>
  <div class="container">
    <div class="player">
      <pre
        v-text="{
          mode,
          playState,
          duration,
          currentTime,
          relPosition,
          liveLatency,
          bandwidth,
        }"
      />
      <div>
        <button @click.prevent="playLive">play live</button>
        <!--
        <button @click.prevent="playUid('EA0E6C02')">play (EA0E6C02)</button>
        <button @click.prevent="playUid('B6DEB689')">play (B6DEB689)</button>
        -->
        <button @click.prevent="pause">pause</button>
        <button @click.prevent="resume">resume</button>
      </div>
      <div>
        <progress
          @click="seek($event.offsetX / $event.currentTarget?.offsetWidth)"
          :max="100"
          :value="relPosition * 100"
        />
      </div>
    </div>
    <div class="queue">
      <div class="spectrum-canvas">
        <canvas ref="canvas" width="21" height="21" />
      </div>
      <div>
        <button @click="pauseDraw">pause</button>
        <button @click="resumeDraw">resume</button>
      </div>
      <pre
        v-text="{
          numQueued: queue.length,
        }"
      />
      <div>
        <button @click.prevent="loadPlaylist('20899A36')">load (20899A36)</button>
      </div>
      <div>
        <div class="media" v-for="media in queue" :key="media.uid">
          <div v-text="media.uid" />
          <div v-text="media.cueIn" />
          <div v-text="media.cueOut" />
          <div v-text="media.fadeIn" />
          <div v-text="media.fadeOut" />
          <div v-text="media.duration" />
          <div>
            <button @click="playMedia(media)">P</button>
          </div>
        </div>
      </div>
    </div>
    <div>
      <div
        :style="{
          height: '50px',
          background: `rgb(${color.join(',')})`,
        }"
      />
      <div class="spectrum" v-if="false">
        <div
          v-for="(b, index) in spectrum"
          :key="`s-${index}`"
          :style="{
            height: `${b / 2.55}px`,
          }"
        />
      </div>
      <div class="spectrum">
        <div
          v-for="(b, index) in spectrum4"
          :key="`s8-${index}`"
          :style="{
            height: `${b}%`,
          }"
        />
      </div>
      <pre
        v-if="media"
        v-text="{
          uid: media.uid,
          duration: media.duration,
        }"
      />
      <pre
        v-text="{
          scope,
          color,
          // spectrum,
        }"
      />
      <pre v-if="true" v-text="debugData" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  padding: 2rem;
}
.player {
  progress {
    width: 100%;
  }
}
.media {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr 1fr 1fr 1fr;
  font-size: 80%;
}
.spectrum {
  height: 100px;
  background: whitesmoke;
  display: flex;
  align-items: flex-end;
  gap: 10px;
  > div {
    width: 20px;
    background: black;
    height: 1px;
    transition: height 50ms;
  }
}

.spectrum-canvas {
  background: white;
  display: inline-flex;
  padding: 10px;
  border: 3px solid black;
  border-radius: 50%;
  > canvas {
    background: white;
  }
}
</style>
