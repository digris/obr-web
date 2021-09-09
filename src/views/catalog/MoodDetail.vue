<script lang="ts">
import {
  computed,
  ref,
  onActivated,
  defineComponent,
} from 'vue';
import { useStore } from 'vuex';

import DetailHeader from '@/components/layout/DetailHeader.vue';
import PlayAction from '@/components/catalog/actions/PlayAction.vue';
import MediaList from '@/components/catalog/media/List.vue';

export default defineComponent({
  components: {
    DetailHeader,
    PlayAction,
    MediaList,
  },
  props: {
    uid: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const store = useStore();
    const isLoaded = ref(false);
    const mood = computed(() => store.getters['catalog/moodByUid'](props.uid));
    const objKey = computed(() => `${mood.value.ct}:${mood.value.uid}`);
    const query = computed(() => ({
      filter: {
        // obj_key: objKey.value,
        tags: [
          '15918360',
          '097413BA',
        ],
      },
      search: [],
      options: {},
    }));
    onActivated(() => {
      if (!mood.value) {
        store.dispatch('catalog/loadMood', props.uid);
      }
    });
    return {
      objKey,
      isLoaded,
      mood,
      query,
    };
  },
});
</script>

<template>
  <div
    v-if="mood"
    class="mood-detail"
  >
    <DetailHeader
      scope="mood"
      :title="mood.name"
    >
      <template
        #visual
      >
        <PlayAction
          :obj-key="objKey"
          :size="(96)"
          :outlined="(false)"
          background-color="rgb(var(--c-white))"
        />
      </template>
      <template
        #info-panel
      >
        (( PANEL ))
      </template>
      <template
        #meta-panel
      >
        (( META ))
      </template>
    </DetailHeader>
    <section
      class="section section--light"
    >
      <div
        class="media-list"
      >
        <MediaList
          :initial-filter="query.filter"
          :disable-user-filter="(false)"
          :disable-play-all="(false)"
        />
      </div>
    </section>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/container";
.section {
  @include container.section;
}
.mood-detail {
  margin-bottom: 12rem;
  .detail-header {
    // TODO: find / define appropriate value...
    min-height: 60vh;
  }
}
.media-list {
  background: rgb(var(--c-white));
}
</style>
