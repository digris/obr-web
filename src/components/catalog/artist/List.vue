<script>
import { getArtists } from '@/api/catalog';

import LoadingMore from '@/components/ui/LoadingMore.vue';
import ArtistCard from './Card.vue';

export default {
  components: {
    LoadingMore,
    ArtistCard,
  },
  data() {
    return {
      artists: [],
      count: 0,
      limit: 16,
      hasNext: false,
      lastOffset: 0,
    };
  },
  methods: {
    // fetchArtists(query) {
    //   this.$store.dispatch('catalog/loadArtists', { query });
    // },
    async fetchArtists(limit = 8, offset = 0) {
      const { count, next, results } = await getArtists(limit, offset);
      this.count = count;
      this.hasNext = !!next;
      this.artists.push(...results);
      // TODO: this kind of smells...
      await this.$store.dispatch('rating/updateObjectRatings', results);
      // this.artists = [...this.artists, ...results];
    },
    fetchNextPage() {
      const offset = this.lastOffset + this.limit;
      this.fetchArtists(this.limit, offset);
      this.lastOffset = offset;
    },
    onEnter() {
      this.fetchNextPage();
    },
  },
  beforeMount() {
    this.artists = [];
    this.fetchArtists();
  },
};
</script>
<template>
  <div class="artist-list">
    <div class="grid">
      <ArtistCard
        v-for="artist in artists"
        :key="artist.uid"
        :artist="artist"
      />
    </div>
    <LoadingMore
      v-if="hasNext"
      :has-next="hasNext"
      @on-enter="fetchNextPage"
    />
  </div>
</template>

<style lang="scss" scoped>
.artist-list {
  margin: 0 0 8rem;
}
.grid {
  display: grid;
  grid-gap: 2rem;
  grid-template-columns: repeat(4, 1fr);
}
</style>
