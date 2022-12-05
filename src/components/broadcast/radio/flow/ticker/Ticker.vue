<script lang="ts" setup>
defineProps({
  text: String,
});
</script>

<template>
  <div class="ticker">
    <div class="ticker__panel">
      <div class="ticker__text" v-text="text" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@keyframes ticker {
  0% {
    transform: translate3d(0, 0, 0);
    visibility: visible;
  }

  100% {
    transform: translate3d(-100%, 0, 0);
  }
}

$duration: 10s;

.ticker {
  overflow-x: hidden;
  display: inline-block;
  pointer-events: none;

  &__panel {
    padding-left: 100%;
    padding-right: 100%;
    animation-iteration-count: infinite;
    animation-timing-function: linear;
    animation-name: ticker;
    animation-duration: $duration;
  }

  &__text {
    color: rgb(var(--c-fg-inverse));
    white-space: nowrap;
  }
}
</style>
