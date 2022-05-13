<script lang="ts">
import { defineComponent } from "vue";
import { useI18n } from "vue-i18n";

import { requireSubscription } from "@/utils/account";
import ContextMenu from "@/components/context-menu/ContextMenu.vue";
import PlayAction from "@/components/catalog/actions/PlayAction.vue";

export default defineComponent({
  components: {
    PlayAction,
    ContextMenu,
  },
  props: {
    filter: {
      type: Object,
      required: false,
      default: () => {},
    },
    ordering: {
      type: Array,
      default: () => [],
    },
    isLoading: {
      type: Boolean,
      default: false,
    },
    numTotal: {
      type: Number,
      default: 0,
    },
  },
  setup() {
    const { t } = useI18n();
    const iconSize = 42;
    const iconColor = "rgb(var(--c-black))";
    const enqueueNext = requireSubscription(async () => {
      console.debug("enqueueNext");
    });
    return {
      t,
      iconSize,
      iconColor,
      enqueueNext,
    };
  },
});
</script>

<template>
  <div
    class="play-all"
    :style="{
      '--c-fg': '0,0,0',
      '--c-bg': '128,128,128',
    }"
    :class="{
      'is-loading': isLoading,
    }"
  >
    <div class="container">
      <div class="play">
        <PlayAction :filter="filter" :ordering="ordering" background-color="rgb(var(--c-white))" />
      </div>
      <div class="info">
        <PlayAction :filter="filter" :ordering="ordering">
          <div v-if="!isLoading" class="text" v-text="t('catalog.list.playAllTracks', numTotal)" />
        </PlayAction>
      </div>
      <div class="actions">
        <ContextMenu
          :list="{
            filter,
            ordering,
          }"
        />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/button";
@use "@/style/elements/container";
.play-all {
  color: rgb(var(--c-black));
  background: rgb(var(--c-gray-500));
  &.is-loading {
    cursor: wait;
  }
}
.container {
  @include container.default;
  display: grid;
  grid-row-gap: 0;
  grid-column-gap: 1rem;
  grid-template-columns: 1fr 16fr 1fr;
  padding-top: 0.75rem;
  padding-bottom: 0.75rem;
  > div {
    display: flex;
    align-items: center;
  }
  .play {
    padding-left: 0;
  }
  .info {
    justify-self: center;
    .text {
      cursor: pointer;
    }
  }
  .actions {
    justify-self: flex-end;
  }
}
</style>
