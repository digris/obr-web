<script lang="ts">
import { computed, defineComponent } from "vue";

export default defineComponent({
  props: {
    playlist: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const title = computed(() => {
      return {
        name: props.playlist.series ? props.playlist.series.name : props.playlist.name,
        appendix: props.playlist.series ? props.playlist.series.episode : null,
      };
    });
    const titleDisplay = computed(() => {
      if (title.value.name && title.value.appendix) {
        return `${title.value.name} #${title.value.appendix}`;
      }
      return title.value.name;
    });
    return {
      titleDisplay,
    };
  },
});
</script>

<template>
  <span v-text="titleDisplay" />
</template>
