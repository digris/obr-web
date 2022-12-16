<script lang="ts">
import AuthPanel from "@/components/account/auth/AuthPanel.vue";
import Page from "@/layouts/Page.vue";

export default {
  components: {
    Page,
    AuthPanel,
  },
  setup() {
    return {};
  },
};
</script>
<template>
  <Page title="Login">
    <section class="section">
      <AuthPanel />
    </section>
  </Page>
</template>

<style lang="scss" scoped>
@use "@/style/elements/section";

.section {
  @include section.default;
}
</style>
