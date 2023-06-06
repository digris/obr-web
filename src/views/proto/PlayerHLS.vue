<script lang="ts" setup>
import { ref } from "vue";

import { getMedia } from "@/api/catalog";
import { usePlayerControls, usePlayerState } from "@/proto/composables/player";

const { mode, playState, duration, currentTime, relPosition, debugData } = usePlayerState();

const { playLive, playMedia, pause, resume, seek } = usePlayerControls();

const queue = ref([]);
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
};
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
          @click="seek($event.offsetX / $event.currentTarget.offsetWidth)"
          :max="100"
          :value="relPosition * 100"
        />
      </div>
    </div>
    <div class="queue">
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
      <pre v-text="debugData" />
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
</style>
