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
import ObjectTags from '@/components/tagging/ObjectTags.vue';
import ObjectIdentifiers from '@/components/identifier/ObjectIdentifiers.vue';
import MediaList from '@/components/catalog/media/List.vue';
import SocialMediaLinks from '@/components/social-media/SocialMediaLinks.vue';

export default defineComponent({
  components: {
    DetailHeader,
    LazyImage,
    PlayAction,
    ObjectTags,
    ObjectIdentifiers,
    MediaList,
    SocialMediaLinks,
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
      :obj-key="objKey"
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
        <ObjectTags
          class="tags"
          :obj="artist"
          :limit="(4)"
        />
        <div
          v-if="artist.countryCode"
        >
          <span
            v-text="artist.countryCode"
          />
          <span
            v-if="artist.dateStart"
          >
            ({{ artist.dateStart.substr(0,4) }})
          </span>
        </div>
        <ObjectIdentifiers
          class="identifiers"
          :obj="artist"
          :limit="(4)"
        />
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
      class="section section--light body"
    >
      <MediaList
        :initial-filter="query.filter"
        :disable-user-filter="(true)"
        :disable-play-all="(true)"
      />
    </section>
    <section
      class="section section--light appendix"
    >
      <SocialMediaLinks />
    </section>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/container";
.section {
  @include container.section;
}
.artist-detail {
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 78px);
  .tags,
  .identifiers {
    margin: .5rem 0;
  }
  .body {
    flex-grow: 1;
  }
  .appendix {
    padding-bottom: 4rem;
  }
}
</style>
