<script lang="ts">
import { defineComponent, ref, computed, onMounted } from "vue";

export default defineComponent({
  props: {
    color: {
      type: Array,
      default: () => [255, 0, 255],
    },
  },
  setup(props) {
    const opacity = ref(0);
    onMounted(() => {
      setTimeout(() => {
        opacity.value = 1.0;
      }, 1);
    });
    const style = computed(() => {
      const bg = props.color.join(",");
      return {
        background: `rgb(${bg})`,
        opacity: opacity.value,
      };
    });
    return {
      style,
    };
  },
});
</script>

<template>
  <div class="visual" :style="style">(( visual ))</div>
</template>

<style lang="scss" scoped>
.visual {
  height: 2000px;
  transition: opacity 200ms;
}
</style>
