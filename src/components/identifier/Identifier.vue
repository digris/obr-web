<script lang="ts">
import { computed, defineComponent } from "vue";

const SCOPE_DISPLAY = {
  wikipedia: "Wikipedia",
  musicbrainz: "Musicbrainz",
  discogs: "Discogs",
  official: "Official website",
};

export default defineComponent({
  props: {
    scope: {
      type: String,
      required: true,
    },
    value: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const title = computed(() => {
      if (props.scope in SCOPE_DISPLAY) {
        // @ts-ignore
        return SCOPE_DISPLAY[props.scope];
      }
      return props.scope;
    });
    return {
      title,
    };
  },
});
</script>

<template>
  <a
    class="identifier"
    :class="`identifier--${scope}`"
    :href="value"
    target="_blank"
    v-text="title"
  />
</template>

<style lang="scss" scoped>
.identifier {
  display: inline-flex;
  white-space: nowrap;
  text-decoration: underline;
}
</style>
