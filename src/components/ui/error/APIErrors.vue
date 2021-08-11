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
        v-else-if="(error.data && error.data.detail)"
        class="error__message"
      >
        {{ error.data.detail }}
      </p>
      <p
        v-else
        class="error__message"
      >
        An error occurred. Sorry.
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
@use "@/style/base/typo";
.errors {
  padding: 1rem;
  color: rgb(var(--c-white));
  background: rgb(var(--c-error));
}
.error {
  position: relative;
  &__message {
    @include typo.bold;
    &:not(:first-child) {
      padding-top: 0.5rem;
    }
  }
  &__status {
    @include typo.dim;
    position: absolute;
    top: 0;
    right: 0;
  }
}
.error:not(:last-child) {
  padding-bottom: 0.5rem;
}
</style>
