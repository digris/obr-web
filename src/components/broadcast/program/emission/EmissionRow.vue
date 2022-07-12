<script lang="ts">
import { computed, defineComponent, ref, onMounted, onUnmounted, onActivated, watch } from "vue";
import { DateTime } from "luxon";
import { getEmission } from "@/api/broadcast";
import { playStream } from "@/player/stream";
import { useObjKey } from "@/composables/obj";

import ButtonPlay from "@/components/player/button/ButtonPlay.vue";
import PlayAction from "@/components/catalog/actions/PlayAction.vue";
import ObjectTags from "@/components/tagging/ObjectTags.vue";
import UserRating from "@/components/rating/UserRating.vue";
import CircleButton from "@/components/ui/button/CircleButton.vue";
import IconPlus from "@/components/ui/icon/IconPlus.vue";
import IconMinus from "@/components/ui/icon/IconMinus.vue";

export default defineComponent({
  components: {
    IconMinus,
    ButtonPlay,
    PlayAction,
    ObjectTags,
    UserRating,
    CircleButton,
    IconPlus,
  },
  props: {
    emission: {
      type: Object,
      required: true,
    },
    isPast: {
      type: Boolean,
      default: false,
    },
    isUpcoming: {
      type: Boolean,
      default: false,
    },
    isCurrent: {
      type: Boolean,
      default: false,
    },
    isExpanded: {
      type: Boolean,
      default: false,
    },
    currentLinkToHome: {
      type: Boolean,
      default: true,
    },
  },
  emits: ["navigate", "toggleExpanded"],
  setup(props, { emit }) {
    // const root = ref(null);
    const root = ref<HTMLElement | null>(null);
    const { objKey } = useObjKey(props.emission.playlist);
    const isHover = ref(false);
    const now = ref(DateTime.now());
    const timer = ref(null);

    const playlist = computed(() => {
      return props.emission.playlist;
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
      if (props.isCurrent) {
        scrollIntoView();
      }
    });
    onMounted(() => {
      if (props.isCurrent) {
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
      () => props.isCurrent,
      async () => {
        if (props.isCurrent) {
          scrollIntoView();
        }
      }
    );
    const routeTo = computed(() => {
      if (props.currentLinkToHome && props.isCurrent) {
        return {
          path: "/",
        };
      }
      if (props.isPast || props.isCurrent) {
        return {
          name: "playlistDetail",
          params: {
            uid: playlist.value.uid,
          },
        };
      }
      return {};
    });
    const play = () => {
      if (props.isCurrent) {
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
    const mediaSet = ref([]);
    // const showMedia = async () => {
    //   props.isExpanded = true;
    //   const data = await getEmission(props.emission.uid);
    //   mediaSet.value = data.mediaSet;
    //   scrollIntoView(true);
    // };
    // const hideMedia = () => {
    //   props.isExpanded = false;
    // };
    watch(
      () => props.isExpanded,
      async (newValue) => {
        if (newValue) {
          const data = await getEmission(props.emission.uid);
          mediaSet.value = data.mediaSet;
          scrollIntoView(true);
        }
      }
    );
    const toggleExpanded = () => {
      emit("toggleExpanded");
    };
    return {
      root,
      objKey,
      isHover,
      routeTo,
      play,
      pause,
      navigate,
      title,
      tagsDisplay,
      timeStartDisplay,
      toggleExpanded,
      mediaSet,
    };
  },
});
</script>

<template>
  <div class="emission-row" @mouseenter="isHover = true" @mouseleave="isHover = false">
    <div class="play">
      <PlayAction
        v-if="isPast"
        :style="{
          '--c-fg': 'var(--c-black)',
          '--c-bg': 'var(--c-white)',
        }"
        :obj-key="`${emission.playlist.ct}:${emission.playlist.uid}`"
      />
      <ButtonPlay
        v-if="isCurrent"
        :style="{
          '--c-fg': 'var(--c-white)',
          '--c-bg': 'var(--c-black)',
        }"
        @play="play"
        @pause="pause"
      />
      <!--
      <ButtonPlay
        v-if="isUpcoming"
        :style="{
          '--c-fg': 'var(--c-black)',
          '--c-bg': 'var(--c-white)',
        }"
        :disabled="true"
      />
      -->
    </div>
    <div class="name">
      <router-link v-if="!isUpcoming" :to="routeTo" @click="navigate">
        {{ title.name }}
        <span v-if="title.appendix" v-text="`#${title.appendix}`" />
      </router-link>
      <span v-else>
        {{ title.name }}
        <span v-if="title.appendix" v-text="`#${title.appendix}`" />
      </span>
    </div>
    <div class="editor" v-if="emission.editor" v-text="emission.editor.name" />
    <ObjectTags class="tags" :obj="emission" :limit="4" />
    <div class="time-start">
      {{ timeStartDisplay }}
    </div>
    <div v-if="isPast || isCurrent" class="actions">
      <CircleButton :size="48" :outlined="false">
        <UserRating
          :obj-key="objKey"
          :icon-size="48"
          :autoload="true"
          :hide-if-unset="!isHover"
          color-var="--c-fg"
        />
      </CircleButton>
      <CircleButton :size="48" @click="toggleExpanded" :outlined="false">
        <IconMinus v-if="isExpanded" :size="48" />
        <IconPlus v-else :size="48" />
      </CircleButton>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/abstracts/responsive";
@use "@/style/elements/container";

.emission-row {
  @include container.default;
  display: grid;
  grid-row-gap: 0;
  grid-column-gap: 1rem;
  grid-template-areas:
    "play name editor  time-start actions"
    "play name tags    time-start actions";
  grid-template-columns: 48px 9fr 8fr 2fr 96px;
  padding: 0.75rem 1.5rem;
  background: rgb(var(--c-bg));

  > div {
    display: flex;
    align-items: center;
  }

  .play {
    position: relative;
    grid-area: play;
    max-height: 48px;
  }

  .name {
    grid-area: name;
    @include typo.large;
    min-width: 0;
    > a,
    > span {
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }
  }

  .editor {
    grid-area: editor;
    overflow: hidden;
  }

  .tags {
    grid-area: tags;
  }

  .time-start {
    grid-area: time-start;
    @include typo.large;
    justify-content: flex-end;
  }

  .actions {
    grid-area: actions;
  }
}
</style>
