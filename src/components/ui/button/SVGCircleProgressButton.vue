<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  props: {
    size: {
      type: Number,
      default: 24,
    },
    active: {
      type: Boolean,
      default: false,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    outlineWidth: {
      type: Number,
      default: 1,
    },
    colorVar: {
      type: String,
      default: '--c-page-fg',
    },
    activeColorVar: {
      type: String,
      default: '--c-page-fg-inverse',
    },
    progress: {
      type: Number,
      default: null,
    },
  },
});
</script>

<template>
  <div
    class="circle-progress-button"
    :style="{
      '--size': `${size}px`,
      '--c-main': `var(${colorVar})`,
      '--c-active': `var(${activeColorVar})`,
    }"
    :class="{
      'is-active': active,
      'is-disabled': disabled,
    }"
  >
    <slot
      name="default"
    />
    <div
      class="progress"
    >
      <svg
        class="progress-circle"
        width="200px"
        height="200px"
        xmlns="http://www.w3.org/2000/svg"
      >
        <circle
          class="progress-circle-back"
          cx="80"
          cy="80"
          r="74"
        ></circle>
        <circle
          class="progress-circle-prog"
          cx="80"
          cy="80"
          r="74"
        ></circle>
      </svg>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.circle-progress-button {
  background: yellow;
}
circle {
  transform: rotate(0.1deg);
  fill: transparent;
  stroke-width: 1.2em;
}

.progress {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 160px;
  height: 160px;
  margin: -80px 0 0 -80px;
  cursor: pointer;
}

.progress-circle {
  margin-top: -40px;
  transform: rotate(-90deg);
}

.progress-circle-back {
  fill: none;
  stroke: #d2d2d2;
  stroke-width:10px;
}

.progress-circle-prog {
  transition: stroke-dasharray 0.7s linear 0s;
  fill: none;
  stroke: #7e3451;
  stroke-width: 10px;
  stroke-dasharray: 100 999;
  stroke-dashoffset: 0px;
}
</style>
