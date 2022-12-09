<script lang="ts">
import { computed, defineComponent } from "vue";

export default defineComponent({
  props: {
    errors: {
      type: Array,
      default: () => [],
    },
    debug: {
      type: Boolean,
      default: false,
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
  <div v-if="hasErrors" class="errors">
    <div v-for="(error, index) in errors" :key="`error-${index}`" class="error">
      <p v-if="error.data && error.data.message" class="error__message">
        {{ error.data.message }}
      </p>
      <p v-else-if="error.data && error.data.detail" class="error__message">
        {{ error.data.detail }}
      </p>
      <p v-else-if="error.message" class="error__message">
        {{ error.message }}
      </p>
      <p v-else class="error__message">An error occurred. Sorry.</p>
      <code v-if="error.status" class="error__status">
        <div class="status-code">#{{ error.status }}</div>
      </code>
      <pre v-if="debug" class="debug" v-text="error" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";

.errors {
  padding: 0.75rem;
  color: rgb(var(--c-black) / 100%);
  background: rgb(var(--c-red) / 60%);
  border-radius: 3px;
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
    @include typo.small;

    top: 4px;
    position: absolute;
    right: 0;
  }
}

.error:not(:last-child) {
  padding-bottom: 0.5rem;
}
</style>
