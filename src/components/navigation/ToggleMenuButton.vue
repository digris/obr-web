<script type="ts">
import { computed,defineComponent } from 'vue';

import CircleButton from '@/components/ui/button/CircleButton.vue';
import IconMenu from '@/components/ui/icon/IconMenu.vue';
import { useAccount } from "@/composables/account";
import { useDevice } from "@/composables/device";

export default defineComponent({
  components: {
    CircleButton,
    IconMenu,
  },
  setup() {
    const { isMobile } = useDevice();
    const { user } = useAccount();
    const initials = computed(() => {
      if (!user.value) {
        return null;
      }
      return (user.value.firstName || user.value.email).substring(0, 1);
    });
    return {
      isMobile,
      user,
      initials,
    };
  },
});
</script>

<template>
  <CircleButton :style="{ position: 'relative' }">
    <IconMenu color-var="--c-page-fg" />
    <div v-if="isMobile && user" class="initials" v-text="initials" />
  </CircleButton>
</template>

<style lang="scss" scoped>
:deep(svg) {
  transition: fill 100ms 1ms, stroke 100ms 1ms;
}

.initials {
  top: 0;
  position: absolute;
  height: 18px;
  width: 18px;
  color: rgb(var(--c-page-fg-inverse));
  background: rgb(var(--c-page-fg));
  pointer-events: none;
  display: flex;
  right: -2px;
  border-radius: 9px;
  padding: 0 6px;
  font-size: 10px;
  align-items: center;
  justify-content: center;
  text-transform: uppercase;
}
</style>
