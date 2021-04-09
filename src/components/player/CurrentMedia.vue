<script lang="ts">
import { defineComponent } from 'vue';

import MediaArtists from '@/components/catalog/media/MediaArtists.vue';

export default defineComponent({
  props: {
    media: {
      type: Object,
      required: true,
      default: () => null,
    },
  },
  components: {
    MediaArtists,
  },
});
</script>

<template>
  <div
    v-if="media"
    class="current-media"
  >
    <div
      class="actions"
    >
      ( P )
    </div>
    <div
      class="metadata"
    >
      <div
        class="metadata--primary"
        :title="media.name"
      >
        {{ media.name }}
      </div>
      <div
        class="metadata--secondary"
      >
        <MediaArtists
          :artists="media.artists"
        />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.current-media {
  display: grid;
  grid-template-columns: 64px 1fr;
  .actions {
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .metadata {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;
    font-size: 0.9rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    &--primary,
    &--secondary {
      max-width: 100%;
      white-space: inherit;
      overflow: inherit;
      text-overflow: inherit;
    }
    &--secondary {
      color: rgba(var(--c-fg), 0.5);
    }
  }
}
</style>
