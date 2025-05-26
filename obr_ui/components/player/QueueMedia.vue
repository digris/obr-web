<script lang="ts" setup>
import { computed, onMounted, ref, watch } from "vue";

import PlayAction from "@/components/catalog/actions/PlayAction.vue";
// import MediaArtists from "@/components/catalog/media/MediaArtists.vue";
import MediaReleases from "@/components/catalog/media/MediaReleases.vue";
import UserRating from "@/components/rating/UserRating.vue";
import CircleButton from "@/components/ui/button/CircleButton.vue";
import IconRemove from "@/components/ui/icon/IconRemove.vue";
import { useQueueControls } from "@/composables/queue";

const props = defineProps({
  objKey: {
    type: String,
    required: true,
  },
  title: {
    type: String,
    default: "",
  },
  artistDisplay: {
    type: String,
    default: "",
  },
  artists: {
    type: Array,
    default: () => [],
  },
  releases: {
    type: Array,
    default: () => [],
  },
  index: {
    type: Number,
    required: true,
  },
  isCurrent: {
    type: Boolean,
    default: false,
  },
});

const root = ref<HTMLElement | null>(null);
const { deleteAtIndex } = useQueueControls();

const canRemove = computed(() => {
  return !props.isCurrent;
});
const remove = async () => {
  await deleteAtIndex(props.index);
};
const scrollIntoView = () => {
  if (!root.value) {
    return;
  }
  try {
    (root.value as any).scrollIntoViewIfNeeded({ block: "end", behavior: "smooth" });
  } catch (e) {
    console.debug(e);
  }
};
onMounted(() => {
  if (props.isCurrent) {
    scrollIntoView();
  }
});
watch(
  () => props.isCurrent,
  async () => {
    if (props.isCurrent) {
      scrollIntoView();
    }
  }
);
</script>

<template>
  <div
    ref="root"
    class="media-row"
    :class="{
      'is-current': isCurrent,
    }"
  >
    <div class="play">
      <PlayAction :obj-key="objKey" :color="[255, 255, 255]" />
    </div>
    <div class="name">
      <span v-text="title" />
    </div>
    <div class="artist">
      <span v-text="artistDisplay" />
      <!--
      <MediaArtists :link="false" :artists="artists" />
      -->
    </div>
    <div class="release">
      <MediaReleases link="false" :releases="releases" />
    </div>
    <div class="actions">
      <CircleButton color-var="--c-light">
        <UserRating color-var="--c-fg" :obj-key="objKey" />
      </CircleButton>
      <CircleButton color-var="--c-fg" @click="remove" :disabled="!canRemove">
        <IconRemove :scale="0.75" />
      </CircleButton>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/base/responsive";

.media-row {
  display: grid;
  grid-row-gap: 0;
  grid-column-gap: 1rem;
  grid-template-areas:
    "play name artist  actions"
    "play name release actions";
  grid-template-columns: 1fr 8fr 5fr 4fr;
  padding: 0.75rem 0;

  > div {
    display: flex;
    align-items: center;
  }

  .play {
    grid-area: play;
    padding-left: 0.5rem;
  }

  .name {
    grid-area: name;

    @include typo.large;

    min-width: 0;

    > span {
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }
  }

  .artist {
    grid-area: artist;
    min-width: 0;

    > span {
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }
  }

  .release {
    grid-area: release;
    min-width: 0;
    overflow: hidden;

    :deep(span) {
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }
  }

  .actions {
    grid-area: actions;
    justify-self: flex-end;
  }

  @include responsive.bp-medium {
    grid-template-areas:
      "play name   actions"
      "play artist actions";
    grid-template-columns: 48px 1fr 96px;
    padding: 0.375rem 0;

    .name {
      @include typo.default;
    }

    .artist {
      @include typo.default;
      @include typo.dim;
      @include typo.light;

      min-width: 0;
      margin-top: -4px; // TODO: just a quick fix
      overflow: hidden;

      > div {
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
      }
    }

    .release,
    .airplays,
    .duration {
      display: none;
    }
  }
}
</style>
