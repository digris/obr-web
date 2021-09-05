<script lang="ts">
import { computed, defineComponent } from 'vue';

export default defineComponent({
  props: {
    tag: {
      type: Object,
      required: true,
    },
    prefix: {
      type: String,
      default: '',
    },
    suffix: {
      type: String,
      default: '',
    },
  },
  setup(props) {
    const display = computed(() => {
      return `${props.prefix}${props.tag.name}${props.suffix}`;
    });
    return {
      display,
    };
  },
});
</script>

<template>
  <div
    class="tag"
    :class="`tag--${tag.type}`"
    v-text="display"
  />
</template>

<style lang="scss" scoped>
.tag {
  display: inline-flex;
  white-space: nowrap;
}
</style>
