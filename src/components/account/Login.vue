<script lang="ts">
import AuthPanel from "@/components/account/AuthPanel.vue";

export default {
  components: {
    AuthPanel,
  },
  setup() {
    return {};
  },
};
</script>
<template>
  <section class="section">
    <AuthPanel />
  </section>
</template>

<style lang="scss" scoped>
@use "@/style/elements/section";
.section {
  @include section.default;
}
</style>
