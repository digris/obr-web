<script lang="ts">
import { defineComponent, ref, computed } from 'vue';

export default defineComponent({
  inheritAttrs: false,
  props: {
    disabled: {
      type: Boolean,
      default: false,
    },
  },
  setup(props, { attrs }) {
    const button = ref(null);
    const isLoading = ref(false);
    const isSuccess = ref(false);
    const hasError = ref(false);
    const width = ref(0);
    const height = ref(0);

    const style = computed(() => {
      if (hasError.value || isLoading.value || isSuccess.value) {
        return {
          width: `${width.value}px`,
          height: `${height.value}px`,
        };
      }
      return {};
    });

    const classes = computed(() => ({
      'is-loading': isLoading.value,
      'is-success': isSuccess.value,
      'has-error': hasError.value,
      'is-disabled': props.disabled,
    }));

    const setSuccess = (displayFor: number) => {
      isSuccess.value = true;
      setTimeout(() => {
        isSuccess.value = false;
      }, displayFor);
    };

    const setError = (displayFor: number) => {
      hasError.value = true;
      setTimeout(() => {
        hasError.value = false;
      }, displayFor);
    };

    const handleClick = async (e: any) => {
      // @ts-ignore
      const rect = button.value.getBoundingClientRect();
      width.value = rect.width;
      height.value = rect.height;
      try {
        isLoading.value = true;
        // @ts-ignore
        await attrs.onClick(e);
        setSuccess(2000);
      } catch (err) {
        console.debug('hm..', err);
        setError(3000);
      } finally {
        isLoading.value = false;
      }
    };

    const computedAttrs = computed(() => ({
      ...attrs,
      onClick: handleClick,
    }));

    return {
      button,
      isLoading,
      isSuccess,
      hasError,
      style,
      classes,
      computedAttrs,
    };
  },
});
</script>

<template>
  <button
    :style="style"
    :class="classes"
    :disabled="(isLoading || disabled)"
    class="async-button"
    ref="button"
    v-bind="computedAttrs"
  >
    <slot
      v-if="isLoading"
      name="loading"
    >
      <svg
        class="loading-spinner"
        width="38"
        height="38"
        viewBox="0 0 38 38"
        xmlns="http://www.w3.org/2000/svg"
        stroke="#fff"
      >
        <g
          fill="none"
          fill-rule="evenodd"
        >
          <g
            transform="translate(1 1)"
            stroke-width="2"
          >
            <circle
              stroke-opacity=".5"
              cx="18"
              cy="18"
              r="18"
            />
            <path d="M36 18c0-9.94-8.06-18-18-18">
              <animateTransform
                attributeName="transform"
                type="rotate"
                from="0 18 18"
                to="360 18 18"
                dur="2s"
                repeatCount="indefinite"
              />
            </path>
          </g>
        </g>
      </svg>
    </slot>
    <slot
      v-else-if="isSuccess"
      name="success"
    >
      OK
    </slot>
    <slot
      v-else-if="hasError"
      name="error"
    >
      Error
    </slot>
    <slot v-else />
  </button>
</template>

<style lang="scss" scoped>
.async-button {
  transition: background-color 300ms ease-in-out, box-shadow 200ms;
  &.has-error {
    background-color: rgb(var(--c-red));
  }
  &.is-loading {
    cursor: wait !important;
  }
  &.is-success {
    box-shadow: 0 0 1px 3px rgba(var(--c-cta-active), 0.1);
  }
  &.is-disabled {
    cursor: wait !important;
    opacity: 0.7;
  }
  .loading-spinner {
    height: 75%;
  }
}
</style>
