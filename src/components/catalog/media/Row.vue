<script>
export default {
  props: {
    media: {
      type: Object,
    },
  },
  computed: {
    duration() {
      return new Date(this.media.duration * 1000).toISOString().substr(11, 8);
    },
  },
};
</script>

<template>
  <div class="media-row">
    <div class="play">
      (P)
    </div>
    <div class="name">
      {{ media.name }}
    </div>
    <div class="artist">
      {{ media.artistDisplay }}
    </div>
    <div class="duration">
      {{ duration }}
    </div>
  </div>
</template>

<style lang="scss" scoped>
.media-row {
  border-bottom: 2px solid rgb(var(--c-live-fg));
  //TODO: find a modular way to handle color / ui transitions
  transition: border-bottom 200ms 1400ms;
  display: grid;
  grid-gap: 1rem;
  grid-template-columns: 1fr 8fr 8fr 2fr;
  padding: 0.75rem 0;
}
</style>
