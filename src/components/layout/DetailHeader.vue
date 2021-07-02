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

      </div>
    </div>
    <div
      class="main"
    >
      <div
        class="t-visual"
      >
        <slot name="visual" />
      </div>
      <div
        class="body"
      >
        <h1
          v-text="title"
        />
        <slot name="info-panel" />
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
        <slot name="meta-panel" />
      </div>
      <div
        class="actions"
      >
        (( actions ))
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/container";
.detail-header {
  .top,
  .main,
  .bottom {
    @include container.default;
  }
  background: #efefef;
  .top,
  .bottom {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
    .actions {
      justify-self: flex-end;
    }
  }
  .main {
    position: relative;
    .t-visual {
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .body {
      position: absolute;
      top: 0;
      h1 {
        font-weight: 500;
        font-size: 4rem;
      }
    }
  }
}
</style>
