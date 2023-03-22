<script lang="ts">
import { computed, defineComponent } from "vue";

export default defineComponent({
  props: {
    filter: {
      type: Object,
      default: () => {},
    },
  },
  setup(props) {
    const hasFilter = computed(() => {
      if (props.filter.q) {
        return true;
      }
      return !!props.filter.tags.length;
    });
    return {
      hasFilter,
    };
  },
});
</script>
<template>
  <div class="no-results">
    <slot name="default">
      <div v-if="hasFilter" class="body body--no-results">
        <!-- TODO: add translations -->
        <p>No results.</p>
        <p>Please refine or <router-link to="">clear</router-link> your search.</p>
      </div>
      <div v-else class="body body--no-favorites">
        <p>You don't have any favorites yet.</p>
        <p>Go ahead and <router-link to="/discover/">discover</router-link> some!</p>
      </div>
    </slot>
  </div>
</template>
<style lang="scss" scoped>
.no-results {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 4rem;
  margin-top: 4rem;
  margin-bottom: 4rem;

  > .body {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-size: var(--t-fs-large);

    a {
      text-decoration: underline;
    }
  }
}
</style>
