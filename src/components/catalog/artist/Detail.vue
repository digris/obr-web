<script>
// import { onBeforeRouteUpdate } from 'vue-router';

export default {
  data() {
    return {
      uid: null,
      isLoaded: false,
    };
  },
  computed: {
    artist() {
      return this.$store.getters['catalog/artistByUid'](this.uid);
    },
    link() {
      return `/discover/artists/${this.artist.uid}/`;
    },
    imageSrc() {
      return `https://picsum.photos/seed/${this.artist.uid}/200`;
    },
  },
  methods: {
    loadArtist() {
      if (!this.artist) {
        this.$store.dispatch('catalog/loadArtist', this.uid);
      }
    },
  },
  created() {
    console.debug(this.$route.params);
    this.uid = this.$route.params.uid;
    this.loadArtist();
    this.$watch(
      () => this.$route.params,
      (to) => {
        if (to && to.uid) {
          this.uid = to.uid;
          this.loadArtist();
        }
      },
    );
  },
  async onBeforeRouteUpdate(to, from) {
    // react to route changes...
    console.debug(to, from);
  },
};
</script>
<template>
  <div class="detail detail--artist">
    (( Artist ))
    <pre
      v-text="artist"
      class="debug"
    />
  </div>
</template>
