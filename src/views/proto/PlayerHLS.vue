<script lang="ts" setup>
// import { defineComponent } from "vue";
import { usePlayer } from "@/composables/playerHls";

const { playByUid, pause, playState, s } = usePlayer();
</script>

<template>
  (( {{ playState }} ))
  <pre v-text="s" />
  <div>
    <!--    <button @click.prevent="load('..')">load</button>-->
    <button @click.prevent="playByUid('EA0E6C02')">play</button>
    <button @click.prevent="pause">pause</button>
  </div>
</template>
