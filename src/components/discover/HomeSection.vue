<script lang="ts">
import { defineComponent, onActivated, onDeactivated, ref } from "vue";

import CircleButton from "@/components/ui/button/CircleButton.vue";
import IconCaret from "@/components/ui/icon/IconCaret.vue";

export default defineComponent({
  components: {
    CircleButton,
    IconCaret,
  },
  props: {
    title: {
      type: String,
      default: "",
    },
  },
  setup() {
    const scrollX = ref(0);
    const listEl = ref();
    const scrollLane = (smooth = false) => {
      console.debug("scroll", smooth);
      listEl.value.scrollTo({
        left: scrollX.value,
        behavior: smooth ? "smooth" : "auto",
      });
    };
    const scrollNext = () => {
      scrollX.value += 400 * 4;
      scrollLane(true);
    };
    const scrollPrevious = () => {
      scrollX.value -= 400 * 4;
      scrollLane(true);
    };
    // scroll-state
    onActivated(() => {
      console.debug("onActivated", scrollX.value);
      if (scrollX.value) {
        listEl.value.scrollTo({
          left: scrollX.value,
        });
      }
    });
    onDeactivated(() => {
      console.debug("onDeactivated", scrollX.value);
    });
    return {
      listEl,
      scrollNext,
      scrollPrevious,
    };
  },
});
</script>

<template>
  <section>
    <header>
      <h2 v-text="title" />
      <nav>
        <CircleButton :scale="1" :disabled="false" @click="scrollPrevious">
          <IconCaret :scale="1" direction="left" />
        </CircleButton>
        <CircleButton :scale="1" :disabled="false" @click="scrollNext">
          <IconCaret :scale="1" direction="right" />
        </CircleButton>
      </nav>
    </header>
    <div class="lane">
      <div class="container" ref="listEl">
        <slot name="default">(( SLOT ))</slot>
      </div>
    </div>
  </section>
</template>

<style lang="scss" scoped>
@use "@/style/base/responsive";
@use "@/style/elements/grid";
@use "@/style/base/mixins";

header {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;

  h2 {
    flex-grow: 1;
    font-size: var(--t-fs-large);
  }
}

.lane {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-flow: column nowrap;

  .container {
    /*
    @include mixins.hide-scrollbar;
    */

    display: flex;
    overflow: auto;
    flex: none;
    gap: 1rem;
    width: 100%;
    flex-flow: row nowrap;
    scroll-snap-type: x mandatory;
  }

  :deep(.card) {
    min-width: 400px;
    scroll-snap-align: start;
  }
}
</style>
