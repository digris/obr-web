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
          <div class="bar loading-placeholder" />
        </div>
        <div class="line line--secondary">
          <div class="bar loading-placeholder" />
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/responsive";

@keyframes loading {
  from {
    left: -100%;
  }

  to {
    left: 100%;
  }
}

/* animated background */
.loading-placeholder {
  position: relative;
  overflow: hidden;

  &::after {
    content: "";
    display: block;
    background: rgb(128 128 128 / 5%);
    top: 0;
    bottom: 0;
    position: absolute;
    height: 100%;
    width: 100%;
    transform: translateX(0);
    animation: 1.5s loading ease-in-out infinite;
  }
}

.loading-grid {
  display: grid;
  grid-column-gap: 0.5rem;
  grid-template-columns: repeat(4, 1fr);
  width: 100%;

  @include responsive.bp-medium {
    grid-row-gap: 2rem;
    grid-column-gap: 0.625rem;
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
          width: 40%;
        }
      }
    }
  }
}
</style>
