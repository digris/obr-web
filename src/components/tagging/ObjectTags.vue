<script lang="ts">
import { computed, defineComponent } from 'vue';
import Tag from './Tag.vue';

export default defineComponent({
  components: {
    Tag,
  },
  props: {
    obj: {
      type: Object,
      required: true,
    },
    prefix: {
      type: String,
      default: '#',
    },
    separator: {
      type: String,
      default: ', ',
    },
    limit: {
      type: Number,
      default: 8,
    },
    spacing: {
      type: String,
      default: '0.5rem',
    },
  },
  setup(props) {
    const keyPrefix = computed(() => {
      return props.obj?.uid;
    });
    const tags = computed(() => {
      return (props.obj && props.obj.tags) ? props.obj.tags.slice(0, props.limit) : [];
    });
    return {
      keyPrefix,
      tags,
    };
  },
});
</script>

<template>
  <div
    class="tags"
    :style="{
      '--spacing': spacing,
    }"
  >
    <Tag
      class="tags__tag"
      v-for="tag in tags"
      :key="`obj-tag-${keyPrefix}-${tag.uid}`"
      :tag="tag"
      :prefix="prefix"
      suffix=""
    />
  </div>
</template>

<style lang="scss" scoped>
.tags {
  &__tag {
    &:not(:last-child) {
      margin-right: var(--spacing);
    }
  }
}
</style>
