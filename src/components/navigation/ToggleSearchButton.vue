<script type="ts">
import { defineComponent } from 'vue';
import CircleButton from '@/components/ui/button/CircleButton.vue';
import IconSearch from '@/components/ui/icon/IconSearch.vue';

export default defineComponent({
  components: {
    CircleButton,
    IconSearch,
  },
  setup() {
    return {};
  },
});
</script>

<template>
  <CircleButton>
    <IconSearch color-var="--c-page-fg" />
  </CircleButton>
</template>

<style lang="scss" scoped>
:deep(svg) {
  transition: fill 100ms 1ms, stroke 100ms 1ms;
}
</style>
