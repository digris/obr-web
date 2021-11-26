<script lang="ts">
import {
  computed,
  defineComponent,
} from 'vue';
import { DateTime } from 'luxon';

import LazyImage from '@/components/ui/LazyImage.vue';
import PlayAction from '@/components/catalog/actions/PlayAction.vue';
import UserRating from '@/components/rating/UserRating.vue';
import RelativeDateTime from '@/components/ui/date/RelativeDateTime.vue';
import PlaylistName from '@/components/catalog/playlist/Name.vue';

export default defineComponent({
  components: {
    LazyImage,
    PlayAction,
    UserRating,
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
    const objKey = computed(() => `${props.playlist.ct}:${props.playlist.uid}`);
    const link = `/discover/playlists/${props.playlist.uid}/`;
    const title = computed(() => {
      return {
        name: (props.playlist.series) ? props.playlist.series.name : props.playlist.name,
        appendix: (props.playlist.series) ? props.playlist.series.episode : null,
      };
    });
    const subtitle = computed(() => {
      if (props.playlist.series) {
        return props.playlist.name;
      }
      return '-';
    });
    const latestEmission = computed(() => {
      return DateTime.fromISO(props.playlist.latestEmission);
    });
    return {
      objKey,
      title,
      subtitle,
      link,
      latestEmission,
    };
  },
});
</script>

<template>
  <div
    class="card card--artist"
  >
    <router-link
      :to="link"
      class="visual"
    >
      <div
        class="visual__image"
      >
        <LazyImage
          :image="playlist.image"
        >
          <PlayAction
            :obj-key="objKey"
            :size="(64)"
            :outlined="(false)"
            background-color="rgb(var(--c-white))"
          />
        </LazyImage>
      </div>
    </router-link>
    <div
      class="meta"
    >
      <div
        class="title"
      >
        <div
          class="primary"
        >
          <router-link
            :to="link"
          >
            <PlaylistName
              :playlist="playlist"
            />
          </router-link>
        </div>
        <div
          class="secondary"
        >
          <div
            v-text="subtitle"
          />
        </div>
        <div
          class="actions"
        >
          <UserRating
            :obj-key="objKey"
          />
        </div>
      </div>
      <div
        class="subtitle"
      >
        <!--<small>{{ latestEmission }}</small>-->
        <RelativeDateTime
          :date-time="latestEmission"
        />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
.card {
  .visual {
    position: relative;
    background: rgba(var(--c-white), .25);
    &__image {
      position: relative;
      width: 100%;
      padding-bottom: 100%;
      .lazy-image {
        position: absolute;
        width: 100%;
      }
    }
  }
  .meta {
    padding: 0.5rem 0 0 0;
    line-height: 1.25rem;
    .title {
      display: grid;
      grid-row-gap: 0.25rem;
      grid-column-gap: 1rem;
      grid-template-areas:
        "primary   actions"
        "secondary actions";
      grid-template-columns: 1fr auto;
      margin-bottom: 0.25rem;
      overflow-wrap: anywhere;
      a {
        flex-grow: 1;
      }
      .primary {
        grid-area: primary;
        font-weight: 600;
        .appendix {
          margin-left: 0.5rem;
        }
      }
      .secondary {
        display: none;
        grid-area: secondary;
      }
      .actions {
        grid-area: actions;
      }
    }
    .subtitle {
      @include typo.dim;
      @include typo.light;
      text-transform: capitalize;
    }
  }
}
</style>
