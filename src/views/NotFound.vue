<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  props: {
    path: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    console.debug("props", props);
  },
});
</script>

<template>
  <div class="not-found">
    <div class="header">
      <div class="title">
        <i18n-t keypath="pages.pageNotFound" tag="h1" />
      </div>
    </div>
    <div class="body">
      <p>{{ path }}</p>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/container";
@use "@/style/elements/detail-header";
.not-found {
  @include container.default;
  margin-bottom: 12rem;
}
.header {
  @include detail-header.default;
}
</style>
