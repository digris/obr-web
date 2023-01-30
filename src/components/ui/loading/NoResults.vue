<template>
  <div class="no-results">
    <slot name="default"> No Results </slot>
  </div>
</template>
<style lang="scss" scoped>
.no-results {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 4rem;
  margin-top: 2rem;
}
</style>
