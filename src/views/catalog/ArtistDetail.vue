<script>
import {
  computed, ref, onMounted, watch,
} from 'vue';
import { useRoute } from 'vue-router';
import { useStore } from 'vuex';

export default {
  setup() {
    const store = useStore();
    const route = useRoute();
    const uid = ref(route.params.uid);
    const isLoaded = ref(false);
    const artist = computed(() => store.getters['catalog/artistByUid'](uid.value));
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
    return {
      uid,
      isLoaded,
      artist,
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
      class="detail-header"
    >
      <div class="title">
        <h1>{{ artist.name }}</h1>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
/* stylelint-disable-next-line at-rule-no-unknown */
@use "@/style/elements/container";
.artist-detail {
  @include container.default;
}
</style>
