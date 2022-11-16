<script lang="ts">
import eventBus from "@/eventBus";

export default {
  setup() {
    const login = () => {
      const event = {
        intent: "login",
      };
      eventBus.emit("account:authenticate", event);
    };
    return {
      login,
    };
  },
};
</script>
<template>
  <section class="section">
    <i18n-t @click.prevent="login" keypath="account.auth.login" tag="button" />
  </section>
</template>

<style lang="scss" scoped>
@use "@/style/elements/section";
.section {
  @include section.default;
}
</style>
