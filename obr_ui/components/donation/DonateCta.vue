<script lang="ts" setup>
import { computed, onMounted, ref, watch } from "vue";
import { useDocumentVisibility, useIntervalFn, useStorage } from "@vueuse/core";

import IconHeart from "@/components/ui/icon/IconHeart.vue";
import { useAccount } from "@/composables/account";
import eventBus from "@/eventBus";

const CTA_SHOW_AGAIN_AFTER = 28 * 24 * 60 * 60 * 1000; // 28 days
const CTA_SHOW_AFTER_SECONDS = 30;

const isVisible = ref(false);

const documentVisible = useDocumentVisibility();
const documentVisibleSeconds = ref(0);
const ctaDismissed = useStorage("donate/ctaDismissed", -1);

const { user } = useAccount();

const hasActiveDonation = computed(() => {
  return !!(user.value?.donations ?? []).find((d: object) => d?.state === "active");
});

const dismiss = () => {
  ctaDismissed.value = Date.now();
  isVisible.value = false;
};

const confirm = () => {
  isVisible.value = false;
  eventBus.emit("donation:showPanel");
};

const { pause, resume } = useIntervalFn(
  () => {
    documentVisibleSeconds.value += 1;
    if (documentVisibleSeconds.value >= CTA_SHOW_AFTER_SECONDS) {
      pause();
      isVisible.value = true;
    }
  },
  1000,
  {
    immediate: false,
  }
);

onMounted(async () => {
  // check if cta was dismissed more than CTA_SHOW_AGAIN_AFTER ago.
  // if so, reset it to -1 to show the cta again.
  if (ctaDismissed.value > 0 && Date.now() - ctaDismissed.value > CTA_SHOW_AGAIN_AFTER) {
    ctaDismissed.value = -1;
  }

  if (ctaDismissed.value > 0) {
    console.debug("CTA was dismissed, not showing it again");
    return;
  }

  // check if user has an active donation
  if (hasActiveDonation.value) {
    console.debug("User has an active donation, not showing CTA");
    return;
  }

  // start timer
  // resume(); // NOTE: disabled until implementation is tested
});

watch(
  () => documentVisible.value,
  (value) => {
    if (value === "hidden") {
      pause();
    } else {
      resume();
    }
  }
);

eventBus.on("donation:showCta", () => {
  isVisible.value = !isVisible.value;
});

eventBus.on("donation:togglePanel", () => {
  // stop the timer if user manually opens the donation panel
  pause();
});
</script>

<template>
  <div v-if="isVisible" class="cta-container">
    <div class="header">
      <div
        class="icon"
        :style="{
          '--c-fg': 'var(--c-red)',
        }"
      >
        <IconHeart :scale="1.25" />
      </div>
      <div class="text">
        <i18n-t keypath="donate.cta.title" tag="h2" />
        <i18n-t keypath="donate.cta.lead" tag="p" />
      </div>
    </div>
    <div class="actions">
      <i18n-t
        keypath="donate.cta.dismiss"
        tag="button"
        @click.prevent="dismiss()"
        class="action action--cancel"
      />
      <div class="separator" />
      <i18n-t
        keypath="donate.cta.confirm"
        tag="button"
        @click.prevent="confirm()"
        class="action action--confirm"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";

@keyframes steam {
  0% {
    background-position: 0 0;
  }

  50% {
    background-position: 400% 0;
  }

  100% {
    background-position: 0 0;
  }
}

.cta-container {
  position: fixed;
  width: 100%;
  color: rgba(var(--c-white) / 100%);
  padding: 0;
  max-width: min(460px, calc(100vw - 2rem));
  bottom: 5.5rem;
  right: 1rem;
  border-radius: 1rem;
  z-index: 15;

  &::before,
  &::after {
    opacity: 0.5;
    top: -2px;
    position: absolute;
    height: calc(100% + 4px);
    width: calc(100% + 4px);
    content: "";
    left: -2px;
    background: linear-gradient(45deg, #f0f, #0ff, #f0f);
    background-size: 400%;
    z-index: -1;
    animation: steam 20s linear infinite;
    border-radius: 1rem;
  }

  &::after {
    filter: blur(10px);
  }

  > .header {
    display: flex;
    align-items: center;
    padding: 0.75rem 0.5rem;
    background: rgba(var(--c-black) / 90%);
    border-radius: 1rem 1rem 0 0;

    > .icon {
      display: flex;
      align-items: center;
      justify-content: center;
    }

    > .text {
      > h2 {
        @include typo.default;
      }

      > p {
        @include typo.default;
        @include typo.light;
      }
    }
  }

  > .actions {
    background: rgba(var(--c-black) / 100%);
    border-radius: 0 0 1rem 1rem;
    padding: 0.75rem 0.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 0.5rem;

    > .action {
      @include typo.default;

      flex: 1;
      background: transparent;
      border: none;
      color: inherit;
      cursor: pointer;

      &--cancel {
        @include typo.light;
        @include typo.dim(0.75);
      }

      &--confirm {
        color: currentcolor;
      }
    }

    > .separator {
      height: 1.5rem;
      width: 1px;
      background: rgba(var(--c-white) / 25%);
    }
  }
}
</style>
