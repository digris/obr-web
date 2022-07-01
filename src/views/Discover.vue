<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  setup() {
    return {};
  },
});
</script>

<template>
  <div class="discover">
    <router-view name="header" />
    <div class="body">
      <router-view v-slot="{ Component }">
        <keep-alive :max="6">
          <component :is="Component" />
        </keep-alive>
      </router-view>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.body {
  padding-bottom: 4rem;
}
</style>
