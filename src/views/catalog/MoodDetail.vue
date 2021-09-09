<script lang="ts">
import {
  computed,
  ref,
  onActivated,
  defineComponent,
} from 'vue';
import { useStore } from 'vuex';

import DetailHeader from '@/components/layout/DetailHeader.vue';
import Filterbar from '@/components/filter/Filterbar.vue';
import PlayAction from '@/components/catalog/actions/PlayAction.vue';
import MediaList from '@/components/catalog/media/List.vue';
import Animation from '@/components/animation/Animation.vue';

export default defineComponent({
  components: {
    DetailHeader,
    Filterbar,
    PlayAction,
    MediaList,
    Animation,
  },
  props: {
    uid: {
      type: String,
      required: true,
    },
    query: {
      type: Object,
      default: () => {},
    },
  },
  setup(props) {
    const store = useStore();
    const isLoaded = ref(false);
    const mood = computed(() => store.getters['catalog/moodByUid'](props.uid));
    const objKey = computed(() => `${mood.value.ct}:${mood.value.uid}`);
    const initialQuery = computed(() => ({
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
      initialQuery,
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
      title-scope="Stimmung"
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
        ...
      </template>
      <template
        #appendix
      >
        <Filterbar />
      </template>
      <template
        #background
      >
        <Animation />
      </template>
    </DetailHeader>
    <section
      class="section section--light"
    >
      <div
        class="media-list"
      >
        <MediaList
          :initial-filter="initialQuery.filter"
          :query="query"
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
  .filterbar {
    flex-grow: 1;
    justify-content: flex-end;
    margin-bottom: 1rem;
  }
}
.media-list {
  background: rgb(var(--c-white));
}
</style>
