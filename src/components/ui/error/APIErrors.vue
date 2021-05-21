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
      <div
        class="error__status"
      >
        <div
          class="status-text"
        >
          {{ error.statusText }}
        </div>
        <div
          class="status-code"
        >
          [{{ error.status }}]
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.errors {
  padding: 0.5rem;
  background: rgba(255, 0, 0, 0.1);
  border-left: 4px solid red;
}
.error {
  &__message {
    padding-bottom: 0.5rem;
  }
  &__status {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    font-size: 85%;
    opacity: 0.5;
    .status-code {
      padding-left: 0.5rem;
    }
  }
}
.error:not(:last-child) {
  padding-bottom: 0.5rem;
}
</style>
