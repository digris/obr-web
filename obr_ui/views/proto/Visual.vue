<script lang="ts" setup>
import { computed, ref, watch } from "vue";
import { useElementSize } from "@vueuse/core";

import Visual from "@/components/catalog/mood/Visual.vue";

const el = ref<HTMLElement | null>(null);
const { width, height } = useElementSize(el);

const json = ref(`{
  "rays": [
    {
      "count": 2,
      "width": 0.1,
      "colors": {
        "inner": [
          0, 0, 0, 0.5
        ],
        "outer": [
          255, 255, 255, 0.5
        ]
      },
      "length": 2000,
      "spread": 2
    },
    {
      "count": 2,
      "width": 2,
      "colors": {
        "inner": [
          0, 0, 0, 0.5
        ],
        "outer": [
          255, 255, 255, 0.5
        ]
      },
      "length": 2000,
      "spread": 2
    }
  ],
  "color": [
    119, 231, 199
  ]
}`);
const visible = ref(true);
const data = computed(() => {
  try {
    return JSON.parse(json.value);
  } catch (e) {
    return {
      rays: [],
      color: [100, 100, 100],
    };
  }
});
const rayConfig = computed(() => data.value?.rays ?? []);
const color = computed(() => data.value?.color ?? [100, 100, 100]);

const redraw = () => {
  visible.value = false;
  setTimeout(() => {
    visible.value = true;
  });
};

watch(() => rayConfig.value, redraw);
</script>

<template>
  <div>
    <div class="container">
      <div ref="el" class="visual">
        <Visual
          v-if="visible"
          :width="width"
          :height="height"
          :offset-y="10"
          :color="color"
          :ray-config="rayConfig"
          :style="{
            height: `${height}px`,
          }"
        />
      </div>
      <div class="data">
        <textarea v-model="json" />
        <button @click.prevent="redraw">update</button>
      </div>
      <div>
        <pre
          class="debug"
          v-text="{
            width,
            height,
          }"
        />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.container {
  padding: 1rem;
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-gap: 1rem;

  > .visual {
    aspect-ratio: 2/1;
  }
  > .data {
    > textarea {
      width: 100%;
      height: 100%;
      font-size: 11px;
    }
  }
}
</style>
