<script type="ts">
import { defineComponent } from 'vue';
import CircleButton from '@/components/ui/button/CircleButton.vue';
import IconClose from '@/components/ui/icon/IconClose.vue';

export default defineComponent({
  components: {
    CircleButton,
    IconClose,
  },
});
</script>

<template>
  <CircleButton
    :size="(32)"
    :outlined="(false)"
  >
    <IconClose
      :size="(32)"
    />
  </CircleButton>
</template>
