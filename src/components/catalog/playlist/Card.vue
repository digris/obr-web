<script lang="ts">
import { computed, defineComponent } from "vue";
import { DateTime } from "luxon";
import { useObjKey } from "@/composables/obj";

import LazyImage from "@/components/ui/LazyImage.vue";
import PlayAction from "@/components/catalog/actions/PlayAction.vue";
import CircleButton from "@/components/ui/button/CircleButton.vue";
import UserRating from "@/components/rating/UserRating.vue";
import ContextMenu from "@/components/context-menu/ContextMenu.vue";
import RelativeDateTime from "@/components/ui/date/RelativeDateTime.vue";
import PlaylistName from "@/components/catalog/playlist/Name.vue";
import { useDevice } from '@/composables/device';

export default defineComponent({
  components: {
    LazyImage,
    PlayAction,
    CircleButton,
    UserRating,
    ContextMenu,
    RelativeDateTime,
    PlaylistName,
  },
  props: {
    playlist: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const { objKey } = useObjKey(props.playlist);
    const link = `/discover/playlists/${props.playlist.uid}/`;
    const latestEmission = computed(() => {
      return DateTime.fromISO(props.playlist.latestEmissionTimeStart);
    });
    const { isDesktop } = useDevice();
    const iconScale = computed(() => {
      return isDesktop.value ? 0.75 : 0.9;
    });
    return {
      objKey,
      link,
      latestEmission,
      iconScale,
    };
  },
});
</script>

<template>
  <div class="card card--playlist">
    <router-link :to="link" class="visual">
      <LazyImage :image="playlist.image">
        <PlayAction
          :obj-key="objKey"
          :icon-scale="1.5"
          :outlined="true"
          :filled="true"
          :color="[0, 0, 0]"
        />
      </LazyImage>
    </router-link>
    <div class="meta">
      <router-link class="title" :to="link">
        <PlaylistName :playlist="playlist" />
      </router-link>
      <RelativeDateTime class="subtitle" :date-time="latestEmission" />
      <div class="actions">
        <CircleButton :scale="iconScale">
          <UserRating :obj-key="objKey" :icon-scale="iconScale" />
        </CircleButton>
        <ContextMenu :obj="playlist" :icon-scale="iconScale" />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/abstracts/responsive";
@use "@/style/base/typo";
@use "@/style/elements/card";
.card {
  @include card.default;
  @include responsive.bp-medium {
    .meta {
      .subtitle {
        @include typo.small;
      }
    }
  }
}
</style>
