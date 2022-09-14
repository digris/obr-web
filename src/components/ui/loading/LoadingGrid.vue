<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  props: {
    number: {
      type: Number,
      default: 4,
    },
  },
});
</script>
<template>
  <div class="loading-grid">
    <div class="card" v-for="(item, index) in Array(number)" :key="`placeholder-${item}-${index}`">
      <div class="card__visual" />
      <div class="card__meta">
        <div class="line line--primary">
          <div class="bar" />
        </div>
        <div class="line line--secondary">
          <div class="bar" />
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/abstracts/responsive";
@keyframes load {
  from {
    left: -150px;
  }
  to {
    left: 100%;
  }
}
.loading-grid {
  display: grid;
  grid-column-gap: 0.5rem;
  grid-template-columns: repeat(4, 1fr);
  width: 100%;
  @include responsive.bp-medium {
    grid-gap: 0.5rem;
    grid-template-columns: repeat(2, 1fr);
  }
}
.card {
  &__visual {
    width: 100%;
    background: rgba(128, 128, 128, 0.1);
    aspect-ratio: 1 / 1;
  }
  &__meta {
    padding: 0.5rem 0 0 0;
    .line {
      position: relative;
      display: flex;
      align-items: center;
      width: 100%;
      height: 1.25rem;
      .bar {
        height: 1rem;
        background: rgba(128, 128, 128, 0.2);
      }
      &--primary {
        .bar {
          width: 60%;
          height: 1.1rem;
        }
      }
      &--secondary {
        .bar {
          width: 24%;
        }
      }
    }
  }
}
</style>
