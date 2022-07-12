<script lang="ts">
import { computed, ref, watch, defineComponent } from "vue";
import { useWindowSize, useFullscreen } from "@vueuse/core";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import eventBus from "@/eventBus";
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
    const root = ref();
    const route = useRoute();
    const router = useRouter();
    const store = useStore();
    const current = computed(() => store.getters["schedule/current"]);
    const next = computed(() => store.getters["schedule/next"]);
    const past = computed(() => store.getters["schedule/past"]);
    const items = computed(() => [next.value || null, current.value || null, ...past.value]);
    const { width: vpWidth, height: vpHeight } = useWindowSize();
    const itemSize = computed(() => {
      const maxForWidth = vpWidth.value * 0.4; // 3/4/3 grid
      const maxForHeight = vpHeight.value - 360; // height - navigation, spacing, player etc.
      // const maxForHeight = vpWidth.value * 0.3; // height - navigation, spacing, player etc.
      // const size = Math.max(Math.min(maxForWidth, maxForHeight, 1200), 240);
      const size = Math.max(Math.min(maxForWidth, maxForHeight, 1200), 240);
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
    const setFocus = (key: string) => {
      console.debug("setFocus", key);
      console.debug("current key", current.value?.key);
      if (current.value?.key === key) {
        focusKey.value = "";
      } else {
        focusKey.value = key;
      }
    };
    const paginate = (offset: number) => {
      if (offset === 0) {
        focusKey.value = "";
      } else {
        const index = calculatedOffset.value + 1 + offset;
        const { key } = items.value[index];
        // focusKey.value = key;
        setFocus(key);
      }
    };
    const releaseFocus = () => {
      console.debug("releaseFocus");
      console.debug("calculatedOffset", calculatedOffset.value);
      for (let i = 0; i < calculatedOffset.value; i += 1) {
        setTimeout(() => {
          paginate(-1);
        }, i * 10);
      }
      // setTimeout(() => {
      //
      // })
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
      // NOTE: for the moment we navigate to the program view
      // programVisible.value = !programVisible.value;
      router.push({
        name: "programRedirect",
        query: { back: "/" },
      });
    };
    const hideProgram = () => {
      programVisible.value = false;
    };
    const stationTimeOverwrite = computed(() => {
      if (!(current.value && focused.value)) {
        return null;
      }
      if (current.value.timeStart === focused.value.timeStart) {
        return null;
      }
      return focused.value.timeStart;
    });
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
    eventBus.on("player:audio:ended", () => {
      if (focusKey.value) {
        console.debug("Radio - audio ended > reset focus lock");
        releaseFocus();
      }
    });
    const { toggle: toggleFullscreen } = useFullscreen();
    return {
      root,
      items,
      itemSize,
      current,
      focusKey,
      focused,
      stationTimeOverwrite,
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
      //
      toggleFullscreen,
    };
  },
});
</script>

<template>
  <div ref="root" class="on-air" :style="cssVars">
    <StationTime
      @release-focus="releaseFocus"
      @toggle-program="toggleProgram"
      :time-overwrite="stationTimeOverwrite"
    />
    <pre
      v-if="false"
      class="debug"
      v-text="{
        focusKey,
      }"
    />
    <div class="left">
      <FocusedEmission
        v-if="focused && focused.emission && focused.playlist"
        :emission="focused.emission"
        :playlist="focused.playlist"
      />
      <PaginateButton :disabled="!hasPrevious" :rotate="180" @click="paginate(1)" />
    </div>
    <div class="center">
      <div
        class="placeholder"
        :style="{
          opacity: current ? 0 : 1,
        }"
      />
    </div>
    <div class="right">
      <FocusedMedia v-if="focused && focused.media" :media="focused.media" :item="focused" />
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
    <Program class="program" :current-link-to-home="false" @navigate="hideProgram" />
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
      height: var(--item-size);
      margin-bottom: 40px;
      background: rgb(var(--c-black));
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
.program {
  margin-bottom: 8rem;
}
</style>
