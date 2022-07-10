<script lang="ts">
import { computed, defineComponent, ref, onMounted, onUnmounted, onActivated, watch } from "vue";
import { DateTime } from "luxon";
import { getEmission } from "@/api/broadcast";
import { getPlaylist } from "@/api/catalog";
import { playStream } from "@/player/stream";
import EmissionRow from "./EmissionRow.vue";
import MediaSet from "./MediaSet.vue";

export default defineComponent({
  components: {
    EmissionRow,
    MediaSet,
  },
  props: {
    emission: {
      type: Object,
      required: true,
    },
    currentLinkToHome: {
      type: Boolean,
      default: true,
    },
  },
  emits: ["navigate"],
  setup(props, { emit }) {
    // const root = ref(null);
    const root = ref<HTMLElement | null>(null);
    const now = ref(DateTime.now());
    const timer = ref(null);
    const isExpanded = ref(false);
    const isPast = computed(() => {
      return props.emission.timeEnd < now.value;
    });
    const isUpcoming = computed(() => {
      return props.emission.timeStart > now.value;
    });
    const isCurrent = computed(() => {
      return props.emission.timeStart < now.value && props.emission.timeEnd > now.value;
    });

    const scrollIntoView = (force = false) => {
      if (!root.value) {
        return;
      }
      if (force) {
        root.value.scrollIntoView({
          block: "start",
          behavior: "smooth",
        });
      } else {
        root.value.scrollIntoViewIfNeeded({
          block: "end",
          behavior: "smooth",
        });
      }
    };
    onActivated(() => {
      if (isCurrent.value) {
        scrollIntoView();
      }
    });
    onMounted(() => {
      if (isCurrent.value) {
        scrollIntoView();
      }
      // @ts-ignore
      timer.value = setInterval(() => {
        now.value = DateTime.now();
      }, 2000);
    });
    onUnmounted(() => {
      // @ts-ignore
      clearInterval(timer.value);
    });
    watch(
      () => isCurrent.value,
      async () => {
        if (isCurrent.value) {
          scrollIntoView();
        }
      }
    );
    const routeTo = computed(() => {
      if (props.currentLinkToHome && isCurrent.value) {
        return {
          path: "/",
        };
      }
      if (isPast.value || isCurrent.value) {
        return {
          name: "playlistDetail",
          params: {
            uid: props.emission.playlist?.uid,
          },
        };
      }
      return {};
    });
    const play = () => {
      if (isCurrent.value) {
        playStream();
      }
      return null;
    };
    const pause = () => {
      console.debug("pause");
    };
    const navigate = () => {
      emit("navigate");
    };
    const title = computed(() => {
      return {
        name: props.emission.series ? props.emission.series.name : props.emission.name,
        appendix: props.emission.series ? props.emission.series.episode : null,
      };
    });
    const tagsDisplay = computed(() => {
      return props.emission.tags.slice(0, 4).join(", ");
    });
    const timeStartDisplay = computed(() => {
      if (!props.emission?.timeStart) {
        return null;
      }
      return props.emission.timeStart.setLocale("de-ch").toLocaleString(DateTime.TIME_24_SIMPLE);
    });
    const cssVars = computed(() => {
      let fg = "var(--c-black)";
      let bg = "var(--c-white)";
      let bgHover = "var(--c-gray-50)";

      if (isExpanded.value) {
        fg = "var(--c-black)";
        bg = "var(--c-gray-100)";
        bgHover = "var(--c-gray-100)";
      }

      if (isCurrent.value) {
        fg = "var(--c-white)";
        bg = "var(--c-black)";
        bgHover = "var(--c-black)";
      }

      if (isUpcoming.value) {
        bg = "var(--c-gray-50)";
        fg = "var(--c-gray-400)";
      }
      return {
        "--c-fg": fg,
        "--c-bg": bg,
        "--c-bg-hover": bgHover,
      };
    });
    const mediaSet = ref([]);
    const loadMediaSet = async () => {
      const mediaSetData = await getEmission(props.emission.uid);
      const playlistData = await getPlaylist(props.emission.playlist.uid);
      const media = [];
      console.debug("mediaSetData", mediaSetData);
      console.debug("playlistData", playlistData);
      playlistData.mediaSet.forEach((m: object) => {
        console.debug("m", m.media.uid);
        const timeStart = mediaSetData.mediaSet.find(
          (msm: object) => msm.mediaUid === m.media.uid
        ).timeStart;
        media.push({
          ...m,
          timeStart,
        });
      });
      console.debug("media", media);
      mediaSet.value = mediaSetData.mediaSet;
    };
    const showMedia = async () => {
      isExpanded.value = true;
      await loadMediaSet();
      scrollIntoView(true);
    };
    const hideMedia = () => {
      isExpanded.value = false;
    };
    const toggleExpanded = () => {
      if (isExpanded.value) {
        hideMedia();
      } else {
        showMedia();
      }
    };
    return {
      root,
      isPast,
      isCurrent,
      isUpcoming,
      routeTo,
      play,
      pause,
      navigate,
      title,
      tagsDisplay,
      timeStartDisplay,
      cssVars,
      isExpanded,
      showMedia,
      hideMedia,
      toggleExpanded,
      mediaSet,
    };
  },
});
</script>

<template>
  <div
    ref="root"
    class="emission"
    :style="cssVars"
    :class="{
      'is-past': isPast,
      'is-current': isCurrent,
      'is-upcoming': isUpcoming,
      'is-expanded': isExpanded,
    }"
  >
    <EmissionRow
      class="emission-row"
      :emission="emission"
      :is-past="isPast"
      :is-current="isCurrent"
      :is-upcoming="isUpcoming"
      :is-expanded="isExpanded"
      @toggle-expanded="toggleExpanded"
    />
    <transition name="slide">
      <MediaSet class="media-set" v-if="mediaSet && isExpanded" :media-set="mediaSet" />
    </transition>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/abstracts/responsive";
@use "@/style/elements/container";

.emission {
  color: rgb(var(--c-fg));
  background-color: rgb(var(--c-bg));
  border-bottom: 1px solid rgb(var(--c-gray-200));
  transition: background 200ms;

  &:hover {
    background: rgb(var(--c-bg-hover));
  }

  /*
  &.is-past {
    color: rgb(var(--c-black));
    //background-color: rgb(var(--c-gray-100));
    &:hover {
      background-color: rgb(var(--c-gray-100));
    }
  }

  &.is-current {
    color: rgb(var(--c-white));
    background-color: rgb(var(--c-black));
    &:hover {
      background-color: rgb(var(--c-gray-900));
    }
  }

  &.is-upcoming {
    color: rgb(var(--c-black));
    background-color: rgb(var(--c-white));
    cursor: default;
    opacity: 0.5;
  }
  */

  &.is-expanded {
    position: relative;
    /*
    color: rgb(var(--c-white));
    background-color: rgb(var(--c-black));
    &:hover {
      background-color: rgb(var(--c-gray-900));
    }
    */
    .emission-row {
      //background: darkorange;
      position: sticky;
      top: 0;
      z-index: 1;
    }
    .media-set {
      position: relative;
      max-height: 100vh;
      overflow: hidden;
      //background: white;
      border-left: solid 0.5rem rgb(var(--c-bg));
      background: rgb(var(--c-white));
      //z-index: 30;
    }
  }
}
</style>
