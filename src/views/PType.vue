<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  components: {},
});
</script>
<template>
  <div
    class="ptype-view"
  >
    <div
      class="stage"
    >
      (( STAGE ))
    </div>
  </div>
</template>
<style lang="scss" scoped>
.ptype-view {
  background: rgb(var(--white));
}
.stage {
  padding: 2rem;
}
</style>
