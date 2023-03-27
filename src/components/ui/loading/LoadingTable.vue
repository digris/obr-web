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
        <div class="play" />
        <div class="name">
          <div class="line">
            <div class="bar loading-placeholder" />
          </div>
        </div>
        <div class="meta">
          <div class="line">
            <div class="bar loading-placeholder" />
          </div>
          <div class="line">
            <div class="bar loading-placeholder" />
          </div>
        </div>
        <div class="actions" />
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

.loading-table {
  width: 100%;
}

.row {
  border-bottom: 1px solid rgb(var(--c-dark) / 20%);

  .container {
    display: grid;
    grid-gap: 1rem;
    grid-template-columns: 48px 16fr 16fr 48px;
    max-width: var(--container-width);
    height: 74px;
    margin-right: auto;
    margin-left: auto;
    padding: 0 1.5rem;
  }

  .line {
    position: relative;
    min-height: var(--t-fs-large);
    width: 100%;
    display: flex;
    align-items: center;

    .bar {
      height: 16px;
      background: rgb(128 128 128 / 10%);
    }
  }

  .name {
    display: flex;
    align-items: center;

    .bar {
      height: 36px;
      width: 90%;
    }
  }

  .meta {
    display: grid;

    .line {
      margin: 2px 0;

      &:first-child {
        align-items: flex-end;
      }

      &:last-child {
        align-items: flex-start;
      }
    }

    .bar {
      width: 40%;
    }
  }

  @include responsive.bp-medium {
    .container {
      grid-template-columns: 40px 1fr 40px;
      grid-template-areas:
        "play name actions"
        "play meta actions";
      height: 61px;
      max-width: unset;
      margin-right: unset;
      margin-left: unset;
      padding: 0 0.625rem;
      grid-row-gap: 0;
    }

    .play {
      grid-area: play;
    }

    .name {
      grid-area: name;
      height: 28px;
      align-items: flex-end;

      .bar {
        height: 20px;
        width: 90%;
      }
    }

    .meta {
      grid-area: meta;
      height: 28px;
      align-items: flex-start;

      .line {
        &:last-child {
          display: none;
        }
      }

      .bar {
        height: 16px;
        width: 90%;
      }
    }

    .actions {
      grid-area: actions;
    }
  }
}
</style>
