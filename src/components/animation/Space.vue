<script lang="ts">
import { computed, defineComponent } from "vue";

export default defineComponent({
  props: {
    color: {
      type: Array,
      required: false,
      default: () => [0, 0, 0],
    },
  },
  setup(props) {
    const cssVars = computed(() => ({
      "--c-star-rgb": props.color.join(","),
    }));
    return {
      cssVars,
    };
  },
});
</script>

<template>
  <div class="space" :style="cssVars">
    <div class="stars"></div>
    <div class="stars"></div>
    <div class="stars"></div>
    <div class="stars"></div>
    <div class="stars"></div>
  </div>
</template>

<style lang="scss">
@keyframes space-animation {
  0% {
    transform: scale(0.5);
    opacity: 0;
    animation-timing-function: ease-in;
  }
  85% {
    transform: scale(2.8);
    opacity: 1;
    animation-timing-function: linear;
  }
  100% {
    transform: scale(3.5);
    opacity: 0;
  }
}
</style>

<style lang="scss" scoped>
.space,
.stars {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  overflow: hidden;
}
.stars {
  /*
  background-image:
    radial-gradient(2px 2px at 20px 30px, #000, rgba(0,0,0,0)),
    radial-gradient(2px 2px at 40px 70px, #fff, rgba(0,0,0,0)),
    radial-gradient(2px 2px at 50px 160px, #ddd, rgba(0,0,0,0)),
    radial-gradient(2px 2px at 90px 40px, #fff, rgba(0,0,0,0)),
    radial-gradient(2px 2px at 130px 80px, #fff, rgba(0,0,0,0)),
    radial-gradient(2px 2px at 160px 120px, #ddd, rgba(0,0,0,0));
  */
  background-image: radial-gradient(
      2px 2px at 20px 30px,
      rgba(var(--c-star-rgb), 1),
      rgba(var(--c-star-rgb), 0.8) 90%,
      rgba(var(--c-star-rgb), 0) 100%
    ),
    radial-gradient(
      2px 2px at 40px 70px,
      rgba(var(--c-star-rgb), 1),
      rgba(var(--c-star-rgb), 0.8) 90%,
      rgba(var(--c-star-rgb), 0) 100%
    ),
    radial-gradient(
      2px 2px at 50px 160px,
      rgba(var(--c-star-rgb), 1),
      rgba(var(--c-star-rgb), 0.8) 90%,
      rgba(var(--c-star-rgb), 0) 100%
    ),
    radial-gradient(
      2px 2px at 90px 40px,
      rgba(var(--c-star-rgb), 1),
      rgba(var(--c-star-rgb), 0.8) 90%,
      rgba(var(--c-star-rgb), 0) 100%
    ),
    radial-gradient(
      2px 2px at 130px 80px,
      rgba(var(--c-star-rgb), 1),
      rgba(var(--c-star-rgb), 0.8) 90%,
      rgba(var(--c-star-rgb), 0) 100%
    ),
    radial-gradient(
      2px 2px at 160px 120px,
      rgba(var(--c-star-rgb), 1),
      rgba(var(--c-star-rgb), 0.8) 90%,
      rgba(var(--c-star-rgb), 0) 100%
    );
  /*
  background-image:
    radial-gradient(circle at 20px 20px, rgba(200,200,200,0.5), rgba(0,0,0,0) 100%),
    radial-gradient(circle at 200px 200px, rgba(200,200,200,0.5), rgba(0,0,0,0) 100%);
  */
  background-repeat: repeat;
  background-size: 200px 200px;
  opacity: 0;
  transition: background-image 5000ms;
  animation: space-animation 5s infinite;
  &:nth-child(1) {
    background-position: 50% 50%;
    animation-delay: 0s;
  }
  &:nth-child(2) {
    background-position: 20% 60%;
    animation-delay: 1s;
  }
  &:nth-child(3) {
    background-position: -20% -30%;
    animation-delay: 2s;
  }
  &:nth-child(4) {
    background-position: 40% -80%;
    animation-delay: 3s;
  }
  &:nth-child(5) {
    background-position: -20% 30%;
    animation-delay: 4s;
  }
}
</style>
