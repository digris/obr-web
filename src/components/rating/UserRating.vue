<script lang="ts">
import { defineComponent, computed } from 'vue';

export default defineComponent({
  props: {
    rating: {
      type: Object,
      required: false,
    },
  },
  setup(props) {
    // const state = ref('stopped');
    // eslint-disable-next-line arrow-body-style
    const value = computed(() => {
      return (props.rating && props.rating.userRating) ? props.rating.userRating : null;
    });
    return {
      value,
    };
  },
});
</script>

<template>
  <div
    class="user-rating"
  >
    {{ value }}
  </div>
</template>

<style lang="scss" scoped>
.user-rating {
  //background: red;
}
</style>
