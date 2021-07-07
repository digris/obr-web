<script>
import { computed } from 'vue';
import { DateTime } from 'luxon';

import LazyImage from '@/components/ui/LazyImage.vue';
import PlayIcon from '@/components/catalog/actions/PlayIcon.vue';
import RelativeDateTime from '@/components/ui/date/RelativeDateTime.vue';

export default {
  components: {
    LazyImage,
    PlayIcon,
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
    const subTitle = computed(() => {
      if (props.playlist.series) {
        return props.playlist.name;
      }
      return '?';
    });
    const latestEmission = computed(() => {
      return DateTime.fromISO(props.playlist.latestEmission);
    });
    return {
      objKey,
      title,
      subTitle,
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
        />
      </div>
      <PlayIcon
        class="visual__play"
        :obj-key="objKey"
      />
    </div>
    <div
      class="meta"
    >
      <div
        class="title"
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
            class="title__appendix"
          />
        </router-link>
        <!--
        <p
          v-text="subTitle"
        />
        -->
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
.card {
  .visual {
    position: relative;
    background: rgba(var(--c-white), .25);
    &__image {
      position: relative;
      width: 100%;
      padding-bottom: 100%;
      img {
        position: absolute;
        width: 100%;
      }
    }
  }
  .meta {
    padding: 0.5rem 0 0 0;
    line-height: 1.25rem;
    .title {
      font-weight: 600;
      overflow-wrap: anywhere;
      &__appendix {
        margin-left: 0.5rem;
        font-weight: 300;
        font-size: 85%;
        opacity: 0.5;
      }
    }
    .subtitle {
      opacity: 0.5;
    }
  }
}
</style>
