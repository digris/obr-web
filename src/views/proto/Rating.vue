<script lang="ts">
import { defineComponent, ref, computed } from "vue";
import CircleButton from "@/components/ui/button/CircleButton.vue";
import IconPType from "@/components/ui/icon/IconPType.vue";
import IconLogo from "@/components/ui/icon/IconLogo.vue";

import { useRatingStore } from "@/stores/rating";

export default defineComponent({
  components: {},
  setup() {
    const objKey = ref("catalog.playlist:9255A232");
    const { voteByObjKey } = useRatingStore();
    // const vote = voteByObjKey(objKey.value);
    const vote = computed(() => {
      return voteByObjKey(objKey.value);
    });
    return {
      objKey,
      vote,
    };
  },
});
</script>
<template>
  <div class="stage">
    <h1>?</h1>
    <input v-model="objKey" :style="{minWidth: '200px'}"/>
    <pre
      v-text="{
        objKey,
        vote,
      }"
    />
  </div>
</template>
<style lang="scss" scoped>
.stage {
  padding: 2rem;
}
</style>
