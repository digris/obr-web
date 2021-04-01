<script>
const COLORS = [
  '20, 100, 20',
  '20, 20, 100',
  '200, 100, 20',
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
      :style="{background: `rgb(${color})`}"
    >
      {{ color }}
    </div>
  </div>
</template>

<style lang="scss" scoped>
.color-chooser {
  position: fixed;
  top: 60px;
  right: 10px;
  .color {
    cursor: pointer;
    padding: 2px 4px;
    margin-bottom: 2px;
  }
}
</style>
