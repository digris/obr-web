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
    <IconSearch :size="48" color="rgb(var(--c-live-fg))" />
  </CircleButton>
</template>
