<script lang="ts">
import { computed, defineComponent } from "vue";

import Tag from "./Tag.vue";

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
      default: "#",
    },
    limit: {
      type: Number,
      default: 8,
    },
    types: {
      type: Array,
      default: () => [],
    },
    separator: {
      type: String,
      default: ", ",
    },
    spacing: {
      type: String,
      default: "0.25rem",
    },
  },
  setup(props) {
    const keyPrefix = computed(() => {
      return props.obj?.uid;
    });
    const tags = computed(() => {
      let objTags = props.obj && props.obj.tags ? props.obj.tags.slice(0, props.limit) : [];
      if (props.types.length) {
        objTags = objTags.filter((tag: any) => props.types.includes(tag.type));
      }
      objTags = objTags.sort((a: any, b: any) => a.name.localeCompare(b.name));
      return objTags;
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
