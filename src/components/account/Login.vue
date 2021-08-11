<script lang="ts">

import eventBus from '@/eventBus';

export default {
  setup() {
    const login = () => {
      const event = {
        intent: 'login',
      };
      eventBus.emit('account:authenticate', event);
    };
    return {
      login,
    };
  },
};
</script>
<template>
  <section
    class="section"
  >
    <button
      @click.prevent="login"
    >Login</button>
  </section>
</template>

<style lang="scss" scoped>
@use "@/style/elements/section";
.section {
  @include section.default;
}
</style>
