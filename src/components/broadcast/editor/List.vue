<script lang="ts">
import { defineComponent, onMounted, ref, computed } from "vue";
import { getEditors } from "@/api/broadcast";

import EditorCard from "./Card.vue";

export default defineComponent({
  components: {
    EditorCard,
  },
  setup() {
    const editors = ref([]);
    const fetchEditors = async (limit = 128, offset = 0) => {
      const { results } = await getEditors(limit, offset);
      // @ts-ignore
      editors.value.push(...results);
    };
    const activeEditors = computed(() => {
      // @ts-ignore
      return editors.value.filter((e) => e.isActive === true);
    });
    const pastEditors = computed(() => {
      // @ts-ignore
      return editors.value.filter((e) => e.isActive === false);
    });
    onMounted(() => {
      fetchEditors();
    });
    return {
      // editors,
      activeEditors,
      pastEditors,
    };
  },
});
</script>
<template>
  <div class="editor-list">
    <div class="grid" v-if="activeEditors.length">
      <EditorCard v-for="editor in activeEditors" :key="editor.uid" :editor="editor" />
    </div>
    <div class="former-editors" v-if="pastEditors.length">
      <div class="subtitle">
        <div>Ehemalige</div>
      </div>
      <div class="grid">
        <EditorCard v-for="editor in pastEditors" :key="editor.uid" :editor="editor" />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/abstracts/responsive";
@use "@/style/elements/container";
.editor-list {
  @include container.default;
  margin-bottom: 0;
}
.grid {
  display: grid;
  grid-row-gap: 2rem;
  grid-column-gap: 0.5rem;
  grid-template-columns: repeat(4, 1fr);
  @include responsive.bp-small {
    grid-gap: 1rem;
    grid-template-columns: repeat(2, 1fr);
  }
}
.former-editors {
  margin-top: 2rem;
  .subtitle {
    margin-bottom: 1rem;
    font-size: 2rem;
  }
}
</style>
