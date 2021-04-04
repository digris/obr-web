<script>
import { getArtists } from '@/api/catalog';
import Intersect from '@/components/utils/intersect';
import ArtistCard from './Card.vue';

export default {
  components: {
    Intersect,
    ArtistCard,
  },
  data() {
    return {
      artists: [],
      count: 0,
      limit: 24,
      hasNext: false,
      lastOffset: 0,
    };
  },
  // computed: {
  //   artists() {
  //     return this.$store.getters['catalog/artists'];
  //   },
  // },
  methods: {
    // fetchArtists(query) {
    //   this.$store.dispatch('catalog/loadArtists', { query });
    // },
    async fetchArtists(limit = 8, offset = 0) {
      const { count, next, results } = await getArtists({ limit, offset });
      this.count = count;
      this.hasNext = !!next;
      this.artists.push(...results);
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
    <intersect
      v-if="hasNext"
      @enter="onEnter"
    >
      <a
        @click="fetchNextPage"
      >Load more...</a>
    </intersect>
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
