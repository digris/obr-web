<script>
// eslint-disable-next-line import/extensions
import Intersect from '@/components/utils/intersect.js';

export default {
  components: {
    Intersect,
  },
  props: {
    hasNext: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    onEnter() {
      this.$emit('onEnter');
    },
  },
};
</script>
<template>
  <intersect
    @enter="onEnter"
    class="loading-more"
  >
    <span>loading</span>
  </intersect>
</template>

<style lang="scss" scoped>
.loading-more {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 4rem;
  margin-top: 2rem;
}
</style>
