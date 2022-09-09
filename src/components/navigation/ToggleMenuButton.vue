<script type="ts">
import { defineComponent } from 'vue';
import CircleButton from '@/components/ui/button/CircleButton.vue';
import IconMenu from '@/components/ui/icon/IconMenu.vue';

export default defineComponent({
  components: {
    CircleButton,
    IconMenu,
  },
  setup() {
    return {};
  },
});
</script>

<template>
  <CircleButton>
    <IconMenu color-var="--c-page-fg" />
  </CircleButton>
</template>

<style lang="scss" scoped>
:deep(svg) {
  transition: fill 100ms 1ms, stroke 100ms 1ms;
}
</style>
