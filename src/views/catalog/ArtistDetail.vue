<script>
import {
  computed, ref, onMounted, watch,
} from 'vue';
import { useRoute } from 'vue-router';
import { useStore } from 'vuex';

import LazyImage from '@/components/UI/LazyImage.vue';
import MediaList from '@/components/catalog/media/List.vue';

export default {
  components: {
    LazyImage,
    MediaList,
  },
  setup() {
    const store = useStore();
    const route = useRoute();
    const uid = ref(route.params.uid);
    const isLoaded = ref(false);
    const artist = computed(() => store.getters['catalog/artistByUid'](uid.value));
    const mediaList = ref([]);
    onMounted(() => {
      store.dispatch('catalog/loadArtist', uid.value);
    });
    watch(
      () => route.params,
      async (newParams) => {
        uid.value = newParams.uid;
        if (uid.value) {
          await store.dispatch('catalog/loadArtist', uid.value);
        }
      },
    );
    // onBeforeRouteUpdate(async (to, from) => {
    //   // only fetch the user if the id changed as maybe only the query or the hash changed
    //   if (to.params.uid !== from.params.uid) {
    //     await store.dispatch('catalog/loadArtist', to.params.uid);
    //     // userData.value = await fetchUser(to.params.id)
    //   }
    // });
    const dummyQuery = {
      filter: [],
      search: [],
      options: {},
    };
    return {
      uid,
      isLoaded,
      artist,
      mediaList,
      dummyQuery,
    };
  },
};
</script>

<template>
  <div
    v-if="artist"
    class="artist-detail"
  >
    <div
      class="header detail-header"
    >
      <div
        class="visual"
      >
        <LazyImage
          :src="`https://picsum.photos/seed/${uid}/500`"
        />
      </div>
      <div
        class="body"
      >
        <div
          class="kind"
        >
          Artist
        </div>
        <div
          class="title"
        >
          <h1>{{ artist.name }}</h1>
        </div>
        <div
          class="tags"
        >
          <span class="tag">#Electronic</span>
          <span class="tag">#Rock</span>
          <router-link
            :to="{
              name: 'artistDetail',
              params: {
                uid: uid,
              },
              query:{
                'filter.duration': 'long',
                'filter.tags': 'techno+hiphop',
              },
              // query: {
              //   filter: JSON.stringify(dummyQuery),
              // },
            }"
          >
            #Techno
          </router-link>
        </div>
        <div
          class="summary"
        >
          <span>125 Tracks</span>
          <span>1h 25m</span>
        </div>
      </div>
      <div
        class="actions">
        <span>+</span>
        <span>-</span>
      </div>
    </div>
    <div
      class="body"
    >
      <MediaList />
    </div>
  </div>
</template>

<style lang="scss" scoped>
/* stylelint-disable-next-line at-rule-no-unknown */
@use "@/style/elements/container";
/* stylelint-disable-next-line at-rule-no-unknown */
@use "@/style/elements/detail-header";
.artist-detail {
  @include container.default;
  margin-bottom: 12rem;
}
.detail-header {
  @include detail-header.default;
  display: grid;
  //grid-template-columns: 220px 1fr auto;
  grid-template-columns: 2fr 4fr 2fr;
  grid-gap: 2rem;
}
.header {
  .visual {
    img {
      background: rgba(255, 255, 255, 0.1);
      min-width: 100%;
      max-width: 100%;
      border-radius: 50%;
    }
  }
  .body {
    padding-top: 1rem;
    display: flex;
    flex-direction: column;
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
    justify-content: flex-end;
    align-items: flex-end;
  }
}
</style>
