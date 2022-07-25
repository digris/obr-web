<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  props: {
    number: {
      type: Number,
      default: 4,
    },
  },
  setup() {},
});
</script>
<template>
  <div class="loading-table">
    <div
      class="row"
      v-for="(item, index) in Array(number)"
      :key="`placeholder-row-${item}-${index}`"
    >
      <div class="container">
        <div class="row__actions" />
        <div class="row__title">
          <div class="line line--primary">
            <div class="bar" />
          </div>
        </div>
        <div class="row__appendix" />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@keyframes load {
  from {
    left: -150px;
  }
  to {
    left: 100%;
  }
}
.loading-table {
  width: 100%;
}
.row {
  border-bottom: 1px solid rgb(var(--c-gray-200));
  .container {
    display: grid;
    grid-gap: 1rem;
    grid-template-columns: 1fr 16fr 1fr;
    max-width: var(--container-width);
    height: 74px;
    margin-right: auto;
    margin-left: auto;
    padding: 0 1.5rem;
  }
  &__title {
    display: flex;
    align-items: center;
    .line {
      position: relative;
      display: flex;
      align-items: center;
      width: 100%;
      height: 1.25rem;
      .bar {
        height: 1rem;
        background: rgba(128, 128, 128, 0.1);
      }
      &--primary {
        .bar {
          width: 80%;
          height: 2rem;
        }
      }
    }
  }
}
</style>
