<template>
  <div class="service">
    <p class="title">
      Get eclectic!<br />
      <!--For music enthusiasts, by music enthusiasts.-->
    </p>
    <ul>
      <li>High-Quality Streaming</li>
      <li>Always up to date</li>
      <li>Listen to the whole catalog when & where<small>*</small> you want!</li>
    </ul>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";

.service {
  .title {
    @include typo.x-large;
    @include typo.bold;
  }

  > ul {
    margin-top: 1rem;
    line-height: 2;
    list-style-position: inside;
  }
}
</style>
