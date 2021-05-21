<script lang="ts">
import { computed, defineComponent } from 'vue';

export default defineComponent({
  props: {
    value: {
      type: String,
      required: true,
    },
    displayDate: {
      type: Boolean,
      default: true,
    },
    displayTime: {
      type: Boolean,
      default: true,
    },
  },
  setup(props) {
    // eslint-disable-next-line arrow-body-style
    const dateDisplay = computed(() => {
      if (!props.displayDate) {
        return null;
      }
      return props.value.substr(0, 10);
    });
    const timeDisplay = computed(() => {
      if (!props.displayTime) {
        return null;
      }
      return props.value.substr(11, 5);
    });
    return {
      dateDisplay,
      timeDisplay,
    };
  },
});
</script>

<template>
  <span
    class="datetime"
  >
    <span
      v-if="dateDisplay"
      class="datetime__date"
    >{{ dateDisplay }}</span>
    <span
      v-if="(dateDisplay && timeDisplay)"
      class="datetime__separator"
    ></span>
    <span
      v-if="timeDisplay"
      class="datetime__time"
    >{{ timeDisplay }}</span>
  </span>
</template>

<style lang="scss" scoped>
.datetime {
  display: inline-flex;
  &__date,
  &__time {
    white-space: nowrap;
  }
  &__separator {
    padding-left: 0.5rem;
  }
}
</style>
