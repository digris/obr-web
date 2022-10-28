<template>
  <div class="service">
    <p class="title">
      Get eclectic!<br />
      For music enthusiasts, by music enthusiasts.
    </p>
    <ul>
      <li>Always up to date</li>
      <li>Listen to the whole catalog when & where<small>*</small> you want!</li>
      <li>Proin imperdiet tempus consectetur.</li>
    </ul>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
.service {
  padding: 2rem 4rem;
  //line-height: 1;
  .title {
    @include typo.large;
    @include typo.bold;
  }
  > ul {
    margin-top: 1rem;
    line-height: 2;
    list-style-position: inside;
  }
}
</style>
