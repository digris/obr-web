<script>
import { computed } from 'vue';
import { DateTime } from 'luxon';

import LazyImage from '@/components/ui/LazyImage.vue';
import PlayAction from '@/components/catalog/actions/PlayAction.vue';
// import PlayIcon from '@/components/catalog/actions/PlayIcon.vue';
import UserRating from '@/components/rating/UserRating.vue';
import RelativeDateTime from '@/components/ui/date/RelativeDateTime.vue';

export default {
  components: {
    LazyImage,
    PlayAction,
    UserRating,
    RelativeDateTime,
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
};
</script>

<template>
  <div
    class="card card--artist"
  >
    <div
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
    </div>
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
            <span
              v-text="title.name"
            />
            <span
              v-if="title.appendix"
              v-text="`#${title.appendix}`"
              class="appendix"
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
      /*
      img {
        position: absolute;
        width: 100%;
      }
      */
    }
    /*
    &__play-action {
      position: absolute;
    }
    */
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
