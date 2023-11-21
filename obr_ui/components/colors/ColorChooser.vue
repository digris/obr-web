<script>
// import { getContrastColor } from '@/utils/color';

const COLORS = [
  [230, 200, 250],
  [10, 30, 20],
  [83, 27, 247],
];

export default {
  setup() {
    const colors = COLORS;
    return {
      colors,
    };
  },
  methods: {
    setColor(color) {
      console.debug("setColor", color);
    },
  },
};
</script>

<template>
  <div class="color-chooser">
    <div
      v-for="(color, index) in colors"
      class="color"
      :key="`color-${index}`"
      @click="setColor(color)"
      :style="{
        background: `rgb(${color.join(' ')} / 100%)`,
      }"
    ></div>
  </div>
</template>

<style lang="scss" scoped>
.color-chooser {
  top: 60px;
  position: fixed;
  right: 10px;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  justify-content: center;

  .color {
    height: 32px;
    width: 32px;
    margin-bottom: 8px;
    cursor: pointer;
    transition: width 100ms;

    &:hover {
      width: 48px;
    }
  }
}
</style>
