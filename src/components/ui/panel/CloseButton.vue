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
    :size="(48)"
  >
    <IconClose
      :size="(48)"
      color="rgb(var(--c-black))"
    />
  </CircleButton>
</template>
