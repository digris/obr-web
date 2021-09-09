<script lang="ts">
import {
  computed,
  defineComponent,
  ref,
  onActivated,
  //
  onBeforeUpdate,
} from 'vue';
import { useStore } from 'vuex';

import DetailHeader from '@/components/layout/DetailHeader.vue';
import LazyImage from '@/components/ui/LazyImage.vue';
import PlayAction from '@/components/catalog/actions/PlayAction.vue';
import MediaList from '@/components/catalog/media/List.vue';

export default defineComponent({
  components: {
    DetailHeader,
    LazyImage,
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
    const artist = computed(() => store.getters['catalog/artistByUid'](props.uid));
    const objKey = computed(() => `${artist.value.ct}:${artist.value.uid}`);
    const query = computed(() => ({
      filter: {
        obj_key: objKey.value,
      },
      search: [],
      options: {},
    }));
    // this is kind of bad. don't know yet how to improve..
    // onActivated is called when component is already in keep-alive router,
    // onBefore is needed to switch between different objects in the already active component.
    // it also needs some ugly bits in the store (see catalog/loadArtist):
    // when the component is in keep-alive, and routing to here from another place both
    // onActivated and onBeforeUpdate will fire ;(
    onActivated(() => {
      if (!artist.value) {
        store.dispatch('catalog/loadArtist', props.uid);
      }
    });
    onBeforeUpdate(() => {
      if (!artist.value) {
        store.dispatch('catalog/loadArtist', props.uid);
      }
    });
    return {
      objKey,
      isLoaded,
      artist,
      query,
    };
  },
});
</script>

<template>
  <div
    v-if="artist"
    class="artist-detail"
  >
    <DetailHeader
      title-scope="Künstler*in"
      :title="artist.name"
    >
      <template
        #visual
      >
        <div
          class="visual"
        >
          <div
            class="image"
          >
            <LazyImage
              :image="artist.image"
            >
              <PlayAction
                :obj-key="objKey"
                :size="(64)"
                :outlined="(false)"
                background-color="rgb(var(--c-white))"
              />
            </LazyImage>
          </div>
        </div>
      </template>
      <template
        #info-panel
      >
        <div>
          USA (1995)
        </div>
        <!--
        <div
          class="tags"
        >
          <span
            class="tag"
          >#Electronic</span>
          <span
            class="tag"
          >#Rock</span>
          <span
            class="tag"
          >#Techno</span>
        </div>
        -->
      </template>
      <template
        #meta-panel
      >
        <span
          v-if="artist"
        >{{ artist.numMedia }} Tracks</span>
        <span>•</span>
        <span>1h 25m</span>
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
          :disable-user-filter="(true)"
          :disable-play-all="(true)"
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
.artist-detail {
  margin-bottom: 12rem;
}
.header {
  .body {
    display: flex;
    flex-direction: column;
    padding-top: 1rem;
    .title {
      margin-top: 2rem;
    }
    .tags,
    .summary {
      margin-top: 1rem;
    }
    .summary {
      display: flex;
      flex-grow: 1;
      align-items: flex-end;
    }
  }
  .actions {
    display: flex;
    align-items: flex-end;
    justify-content: flex-end;
  }
}
</style>
