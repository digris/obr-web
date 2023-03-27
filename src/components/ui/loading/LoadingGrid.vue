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
@use "@/style/base/responsive";

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
    background: rgb(128 128 128 / 10%);
    aspect-ratio: 1 / 1;
  }

  &__meta {
    padding: 0.5rem 0 0;

    .line {
      position: relative;
      height: 1.25rem;
      width: 100%;
      display: flex;
      align-items: center;

      .bar {
        height: 1rem;
        background: rgb(128 128 128 / 20%);
      }

      &--primary {
        .bar {
          height: 1.1rem;
          width: 60%;
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
