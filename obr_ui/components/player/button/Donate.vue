<script lang="ts" setup>
import { useI18n } from "vue-i18n";

import eventBus from "@/eventBus";

const { t } = useI18n();

const onClick = (e: PointerEvent) => {
  if (e.shiftKey) {
    eventBus.emit("donation:showCta");
  } else {
    eventBus.emit("donation:togglePanel");
  }
};
</script>

<i18n lang="yaml">
de:
  title: "Spenden"
en:
  title: "Donate"
</i18n>

<template>
  <div @click="onClick" class="donate">
    <span class="donate__text" v-text="t('title')" />
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/responsive";
@use "@/style/base/typo";

.donate {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 1.5rem;
  border-radius: 0.75rem;
  padding: 0 0.75rem;
  border: 1px solid rgb(var(--c-fg) / 25%);
  transition: border 100ms, background 100ms;
  cursor: pointer;
  min-width: 48px;

  &__text {
    @include typo.small;

    color: rgb(var(--c-fg));
  }

  @include responsive.on-hover {
    background: rgb(var(--c-fg) / 12.5%);
    border-color: transparent;
  }
}
</style>
