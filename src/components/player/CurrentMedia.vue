<template>
  <div
    class="current-media"
  >
    <div
      class="actions"
    >
      ( P )
    </div>
    <div
      class="metadata"
    >
      <div
        class="metadata--primary"
      >
        Rock The Boat
      </div>
      <div
        class="metadata--secondary"
      >
        Inner Circle
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.current-media {
  display: grid;
  grid-template-columns: 64px 1fr;
  .actions {
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .metadata {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;
    font-size: 0.9rem;
    &--secondary {
      color: rgb(var(--c-gray-500));
    }
  }
}
</style>
