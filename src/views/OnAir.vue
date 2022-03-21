<script lang="ts">
/*
  NOTE: THIS COMPONENT IS NOT IN USE - MOVED TO views/Radio.vue
*/

import { computed, ref, watch, defineComponent } from "vue";
import { useStore } from "vuex";
import { useRoute } from "vue-router";

import StationTime from "@/components/broadcast/onair/station-time/StationTime.vue";
import Schedule from "@/components/broadcast/onair/Schedule.vue";
import FocusedEmission from "@/components/broadcast/onair/FocusedEmission.vue";
import FocusedMedia from "@/components/broadcast/onair/FocusedMedia.vue";
import PaginateButton from "@/components/broadcast/onair/button/PaginateNext.vue";
import Rating from "@/components/broadcast/onair/rating/Rating.vue";
import OverlayPanel from "@/components/ui/panel/OverlayPanel.vue";
import Program from "@/components/broadcast/program/Program.vue";

export default defineComponent({
  components: {
    StationTime,
    Schedule,
    FocusedEmission,
    FocusedMedia,
    PaginateButton,
    Rating,
    OverlayPanel,
    Program,
  },
  setup() {
    const route = useRoute();
    const store = useStore();
    const viewport = computed(() => store.getters["ui/viewport"]);
    const current = computed(() => store.getters["schedule/current"]);
    const next = computed(() => store.getters["schedule/next"]);
    const past = computed(() => store.getters["schedule/past"]);
    const items = computed(() => [next.value || null, current.value || null, ...past.value]);
    const itemSize = computed(() => {
      const { width, height } = viewport.value;
      const maxForWidth = width * 0.4; // 3/4/3 grid
      const maxForHeight = height - 360; // height - navigation, spacing, player etc.
      const size = Math.max(Math.min(maxForWidth, maxForHeight, 720), 240);
      return Math.round(size);
    });
    const cssVars = computed(() => ({
      "--size": `${itemSize.value}px`,
      "--item-size": `${itemSize.value}px`,
      "--item-offset": `${itemSize.value * 0.12}px`,
    }));
    const focusKey = ref("");
    const calculatedOffset = computed(() => {
      try {
        const index = items.value.findIndex((i) => i.key === focusKey.value);
        if (index === -1) {
          return 0;
        }
        return index - 1;
      } catch (err) {
        // pass
      }
      return 0;
    });
    const focused = computed(() => {
      // TODO: check implementation
      try {
        return items.value[calculatedOffset.value + 1];
      } catch {
        return null;
      }
    });
    const paginate = (offset: number) => {
      if (offset === 0) {
        focusKey.value = "";
      } else {
        const index = calculatedOffset.value + 1 + offset;
        const { key } = items.value[index];
        focusKey.value = key;
      }
    };
    const setFocus = (key: string) => {
      focusKey.value = key;
    };
    const releaseFocus = () => {
      console.debug("releaseFocus");
      console.debug("calculatedOffset", calculatedOffset.value);
      for (let i = 0; i < calculatedOffset.value; i += 1) {
        setTimeout(() => {
          paginate(-1);
        }, i * 10);
      }
      // setFocus('');
    };
    const paginatedItems = computed(() => {
      const numItems = 10;
      return items.value.slice(calculatedOffset.value, calculatedOffset.value + numItems);
    });
    const hasPrevious = computed(() => {
      return items.value[calculatedOffset.value + 2] !== undefined;
    });
    const hasNext = computed(() => {
      return items.value[calculatedOffset.value - 1] !== undefined;
    });
    const programVisible = ref(false);
    const toggleProgram = () => {
      programVisible.value = !programVisible.value;
    };
    const hideProgram = () => {
      programVisible.value = false;
    };
    watch(
      () => route.name,
      async (newName) => {
        if (newName !== "home") {
          return;
        }
        const item = focused.value;
        if (item && item.media.releases && item.media.releases.length) {
          const { image } = item.media.releases[0];
          if (image && image.rgb) {
            store.dispatch("ui/setPrimaryColor", image.rgb);
          }
        }
      }
    );
    watch(focused, (item) => {
      if (route.name !== "home") {
        return;
      }
      if (item.media.releases && item.media.releases.length) {
        const { image } = item.media.releases[0];
        if (image && image.rgb) {
          store.dispatch("ui/setPrimaryColor", image.rgb);
        }
      }
    });
    return {
      items,
      itemSize,
      current,
      focused,
      next,
      past,
      cssVars,
      paginate,
      paginatedItems,
      hasPrevious,
      hasNext,
      setFocus,
      releaseFocus,
      //
      programVisible,
      toggleProgram,
      hideProgram,
    };
  },
});
</script>

<template>
  <div class="on-air" :style="cssVars">
    <StationTime @release-focus="releaseFocus" @toggle-program="toggleProgram" />
    <div class="left">
      <FocusedEmission
        v-if="focused && focused.emission && focused.playlist"
        :emission="focused.emission"
        :playlist="focused.playlist"
      />
      <PaginateButton :disabled="!hasPrevious" :rotate="180" @click="paginate(1)" />
    </div>
    <div class="center">
      <div class="placeholder" />
    </div>
    <div class="right">
      <FocusedMedia v-if="focused && focused.media" :media="focused.media" />
      <PaginateButton :disabled="!hasNext" @click="paginate(-1)" />
    </div>
    <div class="actions">
      <Rating v-if="focused && focused.media" :media="focused.media" />
    </div>
    <Schedule
      :current="current"
      :items="paginatedItems"
      :item-size="itemSize"
      @on-focus="setFocus"
    />
  </div>
  <OverlayPanel :is-visible="programVisible" @close="hideProgram" title="Heute">
    <Program :current-link-to-home="false" @navigate="hideProgram" />
  </OverlayPanel>
</template>

<style lang="scss" scoped>
@use "@/style/abstracts/responsive";
.on-air {
  position: relative;
  display: grid;
  grid-row-gap: 0.25rem;
  grid-column-gap: 1rem;
  grid-template-areas:
    ". station-time ."
    "left center right"
    ". actions .";
  grid-template-columns: auto var(--item-size) auto;
  .station-time {
    grid-area: station-time;
  }
  .left {
    grid-area: left;
    padding: 1rem;
  }
  .center {
    grid-area: center;
    .placeholder {
      width: var(--item-size);
      height: calc(var(--item-size) + 40px);
    }
  }
  .right {
    grid-area: right;
    padding: 1rem;
  }
  .actions {
    display: flex;
    grid-area: actions;
    align-items: center;
    justify-content: center;
  }
  .left,
  .right {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    .metadata {
      position: absolute;
      top: 12px;
      left: 2rem;
    }
  }
  //TODO: just a quick fix..
  @include responsive.bp-small {
    grid-template-areas:
      "station-time"
      "center"
      "actions";
    grid-template-columns: auto;
    .left,
    .right {
      display: none;
    }
  }
}
</style>
