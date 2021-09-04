<template>
  <div
    class="program"
  >
    <div
      class="title"
    >
      Programm
    </div>
    <div
      class="body"
    >
      (( Program Component ))
    </div>
  </div>
</template>
<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/elements/container";
.program {
  margin-bottom: 12rem;
}
.title {
  @include container.default;
  @include typo.x-large;
  @include typo.bold;
  margin-top: 1rem;
  margin-bottom: 1.5rem;
  text-align: center;
  background: #00e6ff;
}
.body {
  @include container.default;
  background: #6def6d;
}
</style>
