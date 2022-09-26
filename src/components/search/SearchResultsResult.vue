<script lang="ts">
import type { PropType } from "vue";
import type { SearchMediaResult } from "@/typings/api";
import { computed, defineComponent } from "vue";
import LazyImage from "@/components/ui/LazyImage.vue";
import PlayAction from "@/components/catalog/actions/PlayAction.vue";

export default defineComponent({
  components: {
    LazyImage,
    PlayAction,
  },
  props: {
    result: {
      type: Object as PropType<SearchMediaResult>,
      required: true,
    },
  },
  emits: ["update:modelValue"],
  setup(props) {
    const objKey = computed(() => {
      return `${props.result.ct}:${props.result.uid}`;
    });
    const linkTo = computed(() => {
      return {
        name: "mediaDetail",
        params: {
          uid: props.result.uid,
        },
      };
    });
    return {
      objKey,
      linkTo,
    };
  },
});
</script>
<template>
  <div class="search-result">
    <div class="visual">
      <LazyImage :image="result.image">
        <PlayAction
          :obj-key="objKey"
          :icon-scale="0.6"
          :outlined="true"
          :filled="true"
          :color="[0, 0, 0]"
        />
      </LazyImage>
    </div>
    <router-link :to="linkTo" class="meta">
      <div class="title" v-text="result.title" />
      <div class="subtitle" v-text="result.subtitle" />
    </router-link>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/abstracts/responsive";
@use "@/style/base/typo";
.search-result {
  display: grid;
  grid-template-columns: 48px auto;
  gap: 1rem;
  padding: 8px 0;
  .meta {
    display: flex;
    flex-direction: column;
    justify-content: center;
    white-space: nowrap;
    overflow: hidden;
    padding-right: 3rem;
    .title,
    .subtitle {
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .subtitle {
      @include typo.light;
      @include typo.dim;
    }
  }
  @include responsive.on-hover {
    background: rgba(var(--c-black), 0.075);
    border-color: transparent;
  }
}
</style>
