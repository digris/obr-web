<script lang="ts">
import { computed, defineComponent } from "vue";

const DEBUG = false;

export default defineComponent({
  setup() {
    const debugVars = computed(() => {
      return {};
    });
    return {
      visible: DEBUG,
      debugVars,
    };
  },
});
</script>

<template>
  <div v-if="visible" class="debug-panel">
    <pre v-text="debugVars" />
  </div>
</template>

<style lang="scss" scoped>
.debug-panel {
  position: fixed;
  bottom: 80px;
  left: 10px;
  padding: 1rem;
  font-weight: 300;
  font-size: 0.8rem;
  color: #ffffff;
  background: #000;
}
</style>
