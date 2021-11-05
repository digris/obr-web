<script lang="ts">
import {
  defineComponent,
  ref,
  watch,
  onBeforeMount,
} from 'vue';
import { getPage } from '@/api/cms';

export default defineComponent({
  props: {
    path: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const page = ref({});
    const loadPage = async (path: string) => {
      page.value = {};
      try {
        page.value = await getPage(path);
      } catch (err) {
        page.value = {
          title: 'Not found',
          body: err?.message,
        };
      }
    };
    onBeforeMount(async () => {
      await loadPage(props.path);
    });
    watch(
      () => props.path,
      async (path) => {
        await loadPage(path);
      },
    );
    return {
      page,
      // body,
    };
  },
});
</script>

<template>
  <div
    class="page"
  >
    <div
      class="title"
      v-if="page.title"
    >
      <h1
        v-text="page.title"
      />
    </div>
    <div
      class="body"
      v-if="page.body"
      v-html="page.body"
    />
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/elements/container";
@use "@/style/elements/cms";
.page {
  @include container.small;
  .title {
    padding: 1.5rem 0;
    > h1 {
      @include typo.x-large;
      @include typo.bold;
    }
  }
  :deep(.body ) {
    @include cms.content;
    > p {
      line-height: 110%;
      &:first-child {
        @include typo.large;
      }
    }
  }
}
</style>
