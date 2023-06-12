<script lang="ts" setup>
import { computed } from "vue";
import type { AxiosError, AxiosResponse } from "axios";

interface ApiErrorResponse extends AxiosResponse {
  message?: string;
}

interface ApiError extends AxiosError {
  response?: ApiErrorResponse;
}

interface DisplayError {
  message: string;
  code?: string | number;
}

const props = defineProps<{
  errors: Array<string | ApiError>;
}>();

const getErrorMessage = (error: ApiError): string => {
  if (error.response?.data.message) {
    console.debug("error message: error.response.data.message");
    return error.response.data.message;
  }
  if (error.response?.data.detail) {
    console.debug("error message: error.response.data.detail");
    return error.response.data.detail;
  }
  if (error.response?.message) {
    console.debug("error message: error.response.message");
    return error.response.message;
  }
  return error.response?.statusText ?? "An error occurred. Sorry.";
};

const annotateErrors = (errors: Array<string | ApiError>): Array<DisplayError> => {
  const annotatedErrors: Array<DisplayError> = [];
  errors.forEach((error) => {
    if (typeof error === "string") {
      annotatedErrors.push({
        message: error,
      });
    } else {
      console.debug("error.response", error.response);
      annotatedErrors.push({
        message: getErrorMessage(error),
        code: error.response?.status,
      });
    }
  });
  return annotatedErrors;
};

const annotatedErrors = computed(() => {
  return annotateErrors(props.errors);
});

const hasErrors = computed(() => props.errors.length);
</script>
<template>
  <div v-if="hasErrors" class="errors">
    <div v-for="(error, index) in annotatedErrors" :key="`error-${index}`" class="error">
      <p class="message" v-text="error.message" />
      <code v-if="error.code" class="code">
        <span class="status-code" v-text="`#${error.code}`" />
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

  .code {
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
