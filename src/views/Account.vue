<script lang="ts">
import { defineComponent } from "vue";
import { useI18n } from "vue-i18n";

export default defineComponent({
  setup() {
    const { t } = useI18n();
    return {
      t,
    };
  },
});
</script>

<template>
  <div class="account">
    <div class="header">
      <div class="title" v-text="t('account.title')" />
    </div>
    <div class="body">
      <router-view></router-view>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/responsive";
@use "@/style/elements/container";
@use "@/style/base/typo";

.account {
  @include container.small;

  margin-bottom: 4rem;
  flex-grow: 1;
  display: flex;
  flex-direction: column;

  .header {
    @include typo.x-large;

    margin: 2rem 0;
    @include responsive.bp-medium {
      margin: 0.625rem 0;
    }
  }

  .body {
    flex-grow: 1;
    display: flex;
  }
}
</style>
