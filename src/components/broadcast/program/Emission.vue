<script lang="ts">
import { computed, defineComponent, ref, onMounted, onUnmounted, onActivated, watch } from "vue";
import { DateTime } from "luxon";
import { playStream } from "@/player/stream";
import ButtonPlay from "@/components/player/button/ButtonPlay.vue";
import PlayAction from "@/components/catalog/actions/PlayAction.vue";
import ObjectTags from "@/components/tagging/ObjectTags.vue";

export default defineComponent({
  components: {
    ButtonPlay,
    PlayAction,
    ObjectTags,
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
    const root = ref(null);
    const now = ref(DateTime.now());
    const timer = ref(null);
    const isPast = computed(() => {
      return props.emission.timeEnd < now.value;
    });
    const isUpcoming = computed(() => {
      return props.emission.timeStart > now.value;
    });
    const isCurrent = computed(() => {
      return props.emission.timeStart < now.value && props.emission.timeEnd > now.value;
    });

    const scrollIntoView = () => {
      // @ts-ignore
      root.value.scrollIntoViewIfNeeded({
        block: "end",
        behavior: "smooth",
      });
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
    };
  },
});
</script>

<template>
  <div
    ref="root"
    class="emission-row"
    :class="{
      'is-past': isPast,
      'is-current': isCurrent,
      'is-upcoming': isUpcoming,
    }"
  >
    <div class="container">
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
        <ButtonPlay
          v-if="isUpcoming"
          :style="{
            '--c-fg': 'var(--c-black)',
            '--c-bg': 'var(--c-white)',
          }"
          :disabled="true"
        />
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
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/abstracts/responsive";
@use "@/style/elements/container";

.emission-row {
  color: rgb(var(--c-fg));
  background-color: rgb(var(--c-bg));
  border-bottom: 1px solid rgb(var(--c-gray-200));
  transition: background 200ms;

  &:first-child {
    border-top: 1px solid rgb(var(--c-gray-200));
  }

  &:hover {
    background: rgb(var(--c-gray-100));
  }

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
}

.container {
  @include container.default;
  display: grid;
  grid-row-gap: 0;
  grid-column-gap: 1rem;
  grid-template-areas:
    "play name editor  time-start"
    "play name tags    time-start";
  grid-template-columns: 1fr 9fr 8fr 2fr;
  padding: 0.75rem 0.5rem;

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
}
</style>
