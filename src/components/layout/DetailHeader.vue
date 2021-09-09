<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  props: {
    scope: {
      type: String,
      required: false,
      default: null,
    },
    title: {
      type: String,
      required: false,
      default: null,
    },
  },
});
</script>

<template>
  <div
    class="detail-header"
  >
    <div
      class="top"
    >
      <div
        class="back"
      >
        (( back ))
      </div>
      <div
        class="title"
      >
        (( title ))
      </div>
      <div
        class="actions"
      >
        (( actions ))
      </div>
    </div>
    <div
      class="main"
    >
      <div
        class="t-visual"
      >
        <slot
          name="visual"
        />
      </div>
      <div
        class="body"
      >
        <h1
          v-text="title"
        />
        <slot
          name="info-panel"
        />
      </div>
    </div>
    <div
      class="bottom"
    >
      <div
        class="noop"
      >

      </div>
      <div
        class="meta"
      >
        <slot
          name="meta-panel"
        />
      </div>
      <div
        class="actions"
      >

      </div>
    </div>
    <div
      class="background"
    ></div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/elements/container";
@mixin visual {
  height: 50vh;
  min-height: 240px;
  max-height: 500px;
  .image {
    height: 100%;
  }
  img {
    border-radius: 50%;
  }
}

.detail-header {
  position: relative;
  display: flex;
  flex-direction: column;
  .top,
  .main,
  .bottom {
    @include container.default;
    z-index: 3;
  }
  .top {
    position: sticky;
    top: 78px;
  }
  .top,
  .bottom {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    height: 4rem;
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
    .actions {
      justify-self: flex-end;
    }
  }
  .main {
    position: relative;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    .t-visual {
      display: flex;
      align-items: center;
      justify-content: center;
      :deep(.visual) {
        @include visual;
      }
    }
    .body {
      position: absolute;
      top: 0;
      h1 {
        @include typo.x-large;
      }
    }
  }
  .background {
    position: absolute;
    z-index: 2;
    background: linear-gradient(0.25turn, #3f87a6, #ebf8e1, #f69d3c);
    width: 100%;
    height: 100%;
  }
}
</style>
