<script lang="ts" setup>
import { onMounted, ref } from "vue";

import IconHeart from "@/components/ui/icon/IconHeart.vue";
import eventBus from "@/eventBus";

const isVisible = ref(false);

const dismiss = () => {
  isVisible.value = false;
};

const confirm = () => {
  isVisible.value = false;
  eventBus.emit("donation:showPanel");
};

onMounted(async () => {
  setTimeout(() => {
    isVisible.value = true;
  }, 2000);
});

eventBus.on("donation:showCta", () => {
  isVisible.value = !isVisible.value;
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
        <h2>Spende noch heute</h2>
        <p>Deine Unterstützung zählt!</p>
      </div>
    </div>
    <div class="actions">
      <button @click.prevent="dismiss()" class="action action--cancel">Jetzt nicht</button>
      <div class="separator" />
      <button @click.prevent="confirm()" class="action action--confirm">Spenden</button>
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
