<script type="ts">
import { defineComponent } from 'vue';
import CircleButton from '@/components/ui/button/CircleButton.vue';
import IconBack from '@/components/ui/icon/IconBack.vue';

export default defineComponent({
  components: {
    CircleButton,
    IconBack,
  },
});
</script>

<template>
  <CircleButton
    :size="(48)"
  >
    <IconBack
      :size="(48)"
      color="rgb(var(--c-black))"
    />
  </CircleButton>
</template>
