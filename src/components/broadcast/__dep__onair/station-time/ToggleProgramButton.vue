<script type="ts">
import { defineComponent } from 'vue';
import CircleButton from '@/components/ui/button/CircleButton.vue';
import IconProgram from '@/components/ui/icon/IconProgram.vue';

export default defineComponent({
  components: {
    CircleButton,
    IconProgram,
  },
});
</script>

<template>
  <CircleButton>
    <IconProgram color-var="--c-page-fg" />
  </CircleButton>
</template>
