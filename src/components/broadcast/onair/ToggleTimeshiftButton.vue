<script type="ts">
import { defineComponent } from 'vue';
import CircleButton from '@/components/ui/button/CircleButton.vue';
import IconTimeshift from '@/components/ui/icon/IconTimeshift.vue';

export default defineComponent({
  components: {
    CircleButton,
    IconTimeshift,
  },
});
</script>

<template>
  <CircleButton
    :size="(48)"
    :outlined="(false)"
  >
    <IconTimeshift
      :size="(48)"
    />
  </CircleButton>
</template>
