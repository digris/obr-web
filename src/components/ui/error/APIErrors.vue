<script lang="ts">
import { computed, defineComponent } from 'vue';

export default defineComponent({
  props: {
    errors: {
      type: Array,
      default: () => [],
    },
  },
  setup(props) {
    const hasErrors = computed(() => props.errors.length);
    return {
      hasErrors,
    };
  },
});
</script>
<template>
  <div
    v-if="hasErrors"
    class="errors"
  >
    <div
      v-for="(error, index) in errors"
      :key="`error-${index}`"
      class="error"
    >
      <p
        v-if="(error.data && error.data.message)"
        class="error__message"
      >
        {{ error.data.message }}
      </p>
      <p
        v-else
        class="error__message"
      >
        An error occured. Sorry.
      </p>
      <code
        class="error__status"
      >
        <div
          class="status-code"
        >
          {{ error.status }}
        </div>
      </code>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.errors {
  padding: 0.5rem 1rem 0.5rem calc(1rem - 4px);
  background: rgba(var(--c-error), 0.1);
  border-left: 4px solid rgb(var(--c-error));
}
.error {
  position: relative;
  &__message {
    &:not(:first-child) {
      padding-top: 0.5rem;
    }
  }
  &__status {
    position: absolute;
    top: 0;
    right: 0;
    font-size: 90%;
    opacity: 0.75;
  }
}
.error:not(:last-child) {
  padding-bottom: 0.5rem;
}
</style>
