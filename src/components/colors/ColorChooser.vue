<script>
// import { getContrastColor } from '@/utils/color';

const COLORS = [
  [230, 53, 14],
  [247, 231, 64],
  [247, 78, 40],
  [15, 247, 163],
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
      this.$store.dispatch('ui/setTitle', `c-${color.join('-')}`);
      this.$store.dispatch('ui/setPrimaryColor', color);
    },
  },
};
</script>

<template>
  <div
    class="color-chooser"
  >
    <div
      v-for="(color, index) in colors"
      class="color"
      :key="`color-${index}`"
      @click="setColor(color)"
      :style="{
        background: `rgb(${color.join(',')})`,
      }"
    ></div>
  </div>
</template>

<style lang="scss" scoped>
.color-chooser {
  position: fixed;
  top: 60px;
  right: 10px;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  justify-content: center;
  .color {
    cursor: pointer;
    width: 32px;
    height: 32px;
    margin-bottom: 8px;
    transition: width 100ms;
    &:hover {
      width: 48px;
    }
  }
}
</style>
