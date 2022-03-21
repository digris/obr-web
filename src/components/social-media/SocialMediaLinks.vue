<script type="ts">
import { defineComponent } from 'vue';

export default defineComponent({});
</script>

<template>
  <div class="social-media-links">
    <div class="links">
      <a class="link link--twitter" href="#"> T </a>
      <a class="link link--facebook" href="#"> FB </a>
      <a class="link link--youtube" href="#"> YT </a>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.social-media-links {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  .links {
    display: flex;
    .link {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 56px;
      height: 56px;
      margin: 0 0.5rem;
      color: rgb(var(--c-white));
      background: rgb(var(--c-black));
      border-radius: 28px;
    }
  }
}
</style>
