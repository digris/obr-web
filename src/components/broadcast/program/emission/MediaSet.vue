<script lang="ts">
import { defineComponent } from "vue";
import MediaRow from "./MediaRow.vue";

export default defineComponent({
  components: {
    MediaRow,
  },
  props: {
    mediaSet: {
      type: Array,
      required: true,
    },
  },
  setup() {
    return {};
  },
});
</script>

<template>
  <div class="media-set">
    <MediaRow
      v-for="(media, index) in mediaSet"
      :emission-media="media"
      :key="`emission-media-${index}-${media.uid}`"
    />
  </div>
</template>
