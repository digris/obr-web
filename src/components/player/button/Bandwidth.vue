<script lang="ts">
import { computed, defineComponent } from "vue";

import { useAccount } from "@/composables/account";
import { useSettingsStore } from "@/stores/settings";

export default defineComponent({
  setup() {
    const settingsStore = useSettingsStore();
    const { user } = useAccount();
    const maxBandwidth = computed(() => settingsStore.maxBandwidth);
    const modeDisplay = computed(() => {
      return maxBandwidth.value < 720000 ? "Eco" : "HiFi";
    });
    return {
      user,
      modeDisplay,
    };
  },
});
</script>

<template>
  <div v-if="user" class="bandwidth">
    <router-link :to="{ name: 'accountSettings' }" class="bandwidth__text" v-text="modeDisplay" />
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/responsive";
@use "@/style/base/typo";

.bandwidth {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 1.5rem;
  border-radius: 0.75rem;
  padding: 0 0.75rem;
  border: 1px solid rgb(var(--c-fg) 0.25);
  transition: border 100ms, background 100ms;
  cursor: pointer;
  min-width: 48px;

  &__text {
    @include typo.small;

    color: rgb(var(--c-fg));
  }
  @include responsive.on-hover {
    background: rgb(var(--c-fg) 0.125);
    border-color: transparent;
  }
}
</style>
