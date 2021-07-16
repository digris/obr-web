<script lang="ts">
import {
  defineComponent,
  onMounted,
  ref,
} from 'vue';
import { getEditors } from '@/api/broadcast';

import EditorCard from './Card.vue';

export default defineComponent({
  components: {
    EditorCard,
  },
  props: {
    primaryColor: {
      type: Array,
      default: null,
    },
  },
  setup() {
    const editors = ref([]);
    const fetchEditors = async (limit = 16, offset = 0) => {
      const { results } = await getEditors(limit, offset);
      // @ts-ignore
      editors.value.push(...results);
    };
    onMounted(() => {
      fetchEditors();
    });
    return {
      editors,
    };
  },
});
</script>
<template>
  <div class="editor-list">
    <div class="grid">
      <EditorCard
        v-for="editor in editors"
        :key="editor.uid"
        :editor="editor"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/abstracts/responsive";
@use "@/style/elements/container";
.editor-list {
  @include container.default;
  margin-bottom: 8rem;
}
.grid {
  display: grid;
  grid-gap: 2rem;
  grid-template-columns: repeat(4, 1fr);
  @include responsive.bp-small {
    grid-gap: 1rem;
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
