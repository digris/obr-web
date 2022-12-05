<script lang="ts">
import { DateTime } from "luxon";
import { computed, defineComponent } from "vue";

import PlayAction from "@/components/catalog/actions/PlayAction.vue";
import PlaylistName from "@/components/catalog/playlist/Name.vue";
import ContextMenu from "@/components/context-menu/ContextMenu.vue";
import UserRating from "@/components/rating/UserRating.vue";
import CircleButton from "@/components/ui/button/CircleButton.vue";
import RelativeDateTime from "@/components/ui/date/RelativeDateTime.vue";
import LazyImage from "@/components/ui/LazyImage.vue";
import { useDevice } from "@/composables/device";
import { useObjKey } from "@/composables/obj";

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
    const { isDesktop } = useDevice();
    const link = `/discover/playlists/${props.playlist.uid}/`;
    const latestEmission = computed(() => {
      return DateTime.fromISO(props.playlist.latestEmissionTimeStart);
    });
    return {
      objKey,
      isDesktop,
      link,
      latestEmission,
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
      <UserRating
        v-if="!isDesktop"
        :obj-key="objKey"
        :readonly="true"
        :hide-if-unset="true"
        class="rating"
      />
    </router-link>
    <div class="meta">
      <router-link class="title" :to="link">
        <PlaylistName :playlist="playlist" />
      </router-link>
      <RelativeDateTime class="subtitle" :date-time="latestEmission" />
      <div v-if="isDesktop" class="actions">
        <CircleButton :scale="0.75">
          <UserRating :obj-key="objKey" :icon-scale="0.75" />
        </CircleButton>
        <ContextMenu :obj="playlist" :icon-scale="0.75" />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/responsive";
@use "@/style/base/typo";
@use "@/style/elements/card";

.card {
  @include card.default;
  @include card.actions-on-hover;
}
</style>
