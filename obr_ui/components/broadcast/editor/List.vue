<script lang="ts">
import { computed, defineComponent, onMounted, ref } from "vue";

import { getEditors } from "@/api/broadcast";
import SocialMediaLinks from "@/components/social-media/SocialMediaLinks.vue";
import { useRatingStore } from "@/stores/rating";

import EditorCard from "./Card.vue";

export default defineComponent({
  components: {
    EditorCard,
    SocialMediaLinks,
  },
  setup() {
    const { injectRatings } = useRatingStore();
    const editors = ref([]);
    const fetchEditors = async (limit = 128, offset = 0) => {
      const { results } = await getEditors(limit, offset);
      // @ts-ignore
      editors.value.push(...results);
      await injectRatings(results);
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
    <!--
    <div class="former-editors" v-if="pastEditors.length">
      <div class="subtitle">
        <div>Ehemalige</div>
      </div>
      <div class="grid">
        <EditorCard v-for="editor in pastEditors" :key="editor.uid" :editor="editor" />
      </div>
    </div>
    -->
    <SocialMediaLinks />
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/responsive";
@use "@/style/elements/container";
@use "@/style/elements/grid";

.editor-list {
  @include container.default;

  /* margin-bottom: 4rem; */
}

.social-media-links {
  margin-top: 4rem;
}

.grid {
  @include grid.default;
}

/*
.former-editors {
  margin-top: 2rem;
  .subtitle {
    margin-bottom: 1rem;
    font-size: 2rem;
  }
}
*/
</style>
