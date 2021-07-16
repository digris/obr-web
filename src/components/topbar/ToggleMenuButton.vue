<script type="ts">
import { defineComponent } from 'vue';
import CircleButton from '@/components/ui/button/CircleButton.vue';
import IconMenu from '@/components/ui/icon/IconMenu.vue';

export default defineComponent({
  components: {
    CircleButton,
    IconMenu,
  },
});
</script>

<template>
  <CircleButton
    :size="(48)"
    :outlined="(false)"
  >
    <IconMenu
      :size="(48)"
    />
  </CircleButton>
</template>
