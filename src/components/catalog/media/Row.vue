<script lang="ts">
import { defineComponent, ref, computed } from "vue";
import { DateTime } from "luxon";
import { useObjKey } from "@/composables/obj";

import CircleButton from "@/components/ui/button/CircleButton.vue";
import ContextMenu from "@/components/context-menu/ContextMenu.vue";
import PlayAction from "@/components/catalog/actions/PlayAction.vue";
import MediaArtists from "@/components/catalog/media/MediaArtists.vue";
import MediaReleases from "@/components/catalog/media/MediaReleases.vue";
import UserRating from "@/components/rating/UserRating.vue";
import RelativeDateTime from "@/components/ui/date/RelativeDateTime.vue";
import Duration from "@/components/ui/time/Duration.vue";

export default defineComponent({
  components: {
    CircleButton,
    ContextMenu,
    PlayAction,
    MediaArtists,
    MediaReleases,
    UserRating,
    RelativeDateTime,
    Duration,
  },
  props: {
    media: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const { objKey } = useObjKey(props.media);
    const isHover = ref(false);
    const release = computed(() => {
      return props.media.releases && props.media.releases.length ? props.media.releases[0] : null;
    });
    const latestAirplay = computed(() => {
      if (!props.media.latestAirplay) {
        return null;
      }
      return DateTime.fromISO(props.media.latestAirplay);
    });
    const color = computed(() => {
      return release.value && release.value.image ? release.value.image.rgb : null;
    });
    return {
      objKey,
      isHover,
      release,
      color,
      latestAirplay,
    };
  },
});
</script>

<template>
  <div class="media-row" @mouseenter="isHover = true" @mouseleave="isHover = false">
    <div class="container">
      <div class="play">
        <PlayAction :obj-key="objKey" :outlined="true" :color="[0, 0, 0]" />
      </div>
      <div class="name">
        <router-link
          :to="{
            name: 'mediaDetail',
            params: {
              uid: media.uid,
            },
          }"
          v-text="media.name"
        />
      </div>
      <div class="artist">
        <MediaArtists :artists="media.artists" />
      </div>
      <div class="release">
        <MediaReleases :releases="media.releases" />
      </div>
      <div class="airplays">
        <RelativeDateTime v-if="latestAirplay" :date-time="latestAirplay" />
      </div>
      <Duration class="duration" :seconds="media.duration" />
      <div class="actions">
        <CircleButton>
          <UserRating :obj-key="objKey" :hide-if-unset="!isHover" />
        </CircleButton>
        <ContextMenu :obj="media" />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/abstracts/responsive";
@use "@/style/elements/container";

.media-row {
  border-bottom: 1px solid rgb(var(--c-gray-200));
  transition: background 200ms;

  &:first-child {
    border-top: 1px solid rgb(var(--c-gray-200));
  }

  @include responsive.on-hover {
    background: rgb(var(--c-gray-100));
  }
}

.container {
  @include container.default;
  display: grid;
  grid-row-gap: 0;
  grid-column-gap: 1rem;
  grid-template-areas:
    "play name artist  duration actions"
    "play name release airplays actions";
  grid-template-columns: 96px 8fr 6fr 2fr 96px;
  padding-top: 0.75rem;
  padding-bottom: 0.75rem;
  color: rgb(var(--c-black));
  //TODO: find a modular way to handle color / ui transitions
  transition: border-bottom 200ms 1400ms, color 200ms, background 200ms;

  > div {
    display: flex;
    align-items: center;
  }

  .play {
    position: relative;
    grid-area: play;
  }

  .name {
    grid-area: name;
    @include typo.large;
    min-width: 0;
    margin-left: -48px;
    > a {
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }
  }

  .artist {
    grid-area: artist;
    overflow: hidden;
    > div {
      overflow: hidden;
    }
  }

  .release {
    grid-area: release;
    min-width: 0;
    //overflow: hidden;
    > div {
      overflow: hidden;
      //white-space: nowrap;
      //text-overflow: ellipsis;
    }
  }

  .airplays {
    grid-area: airplays;
  }

  .duration {
    grid-area: duration;
  }

  .actions {
    grid-area: actions;
    justify-self: flex-end;
  }
  // TODO: responsive styles have to be cleaned up
  @include responsive.bp-small {
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
      margin-top: -4px; //TODO: just a quick fix
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
