<script lang="ts">
import { computed, defineComponent, ref } from "vue";
import { DateTime } from "luxon";

import PlayAction from "@/components/catalog/actions/PlayAction.vue";

export default defineComponent({
  components: {
    PlayAction,
  },
  props: {
    emissionMedia: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const isHover = ref(false);
    const media = computed(() => {
      return props.emissionMedia;
    });
    const objKey = computed(() => {
      return `catalog.media:${media.value.mediaUid}`;
    });
    const timeStart = computed(() => {
      return DateTime.fromISO(media.value.timeStart);
    });
    const timeStartDisplay = computed(() => {
      return timeStart.value.setLocale("de-ch").toLocaleString(DateTime.TIME_24_SIMPLE);
    });
    return {
      media,
      objKey,
      isHover,
      timeStartDisplay,
    };
  },
});
</script>

<template>
  <div class="media-row" @mouseenter="isHover = true" @mouseleave="isHover = false">
    <div class="play">
      <PlayAction
        :obj-key="objKey"
        :size="48"
        :outlined="false"
        background-color="rgb(var(--c-white))"
      />
    </div>
    <div class="name">
      <span>{{ media.uid }}</span>
    </div>
    <!--
    <div class="artist">
      <MediaArtists :artists="media.artists" />
    </div>
    <div class="release">
      <MediaReleases :releases="media.releases" />
    </div>
    <div class="actions">
      <CircleButton :size="48" :outlined="false">
        <UserRating :obj-key="objKey" :icon-size="48" :hide-if-unset="!isHover" />
      </CircleButton>
      <ContextMenu :obj="media" />
    </div>
    -->
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/abstracts/responsive";
@use "@/style/elements/container";

.media-row {
  @include container.default;
  display: grid;
  grid-row-gap: 0;
  grid-column-gap: 1rem;
  grid-template-areas:
    "play name editor  time-start actions"
    "play name tags    time-start actions";
  grid-template-columns: 48px 9fr 8fr 2fr 96px;
  padding: 0.75rem 1.5rem 0.75rem 1rem;

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
