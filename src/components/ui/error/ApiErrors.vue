<script lang="ts" setup>
import { computed } from "vue";

interface ErrorData {
  message?: string;
  detail?: string;
}

interface Error {
  data?: ErrorData;
  status?: string;
  message?: string;
}

const props = defineProps<{
  errors: Array<Error>;
}>();

const hasErrors = computed(() => props.errors.length);
</script>
<template>
  <div v-if="hasErrors" class="errors">
    <div v-for="(error, index) in errors" :key="`error-${index}`" class="error">
      <p v-if="error.data && error.data.message" class="message">
        {{ error.data.message }}
      </p>
      <p v-else-if="error.data && error.data.detail" class="message">
        {{ error.data.detail }}
      </p>
      <p v-else-if="error.message" class="message">
        {{ error.message }}
      </p>
      <p v-else class="error__message">An error occurred. Sorry.</p>
      <code v-if="error.status" class="status">
        <div class="status-code">#{{ error.status }}</div>
      </code>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";

.errors {
  padding: 0.75rem;
  color: rgb(var(--c-dark) / 100%);
  background: rgb(var(--c-red) / 60%);
  border-radius: 3px;
}

.error {
  position: relative;

  .message {
    @include typo.bold;

    &:not(:first-child) {
      padding-top: 0.5rem;
    }
  }

  .status {
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
