<template>
  <div
    class="main-menu"
  >
    <router-link
      to="/"
    >
      Radio
    </router-link>
    <router-link
      to="/discover/"
    >
      Discover
    </router-link>
    <router-link
      to="/collection/"
    >
      Favoriten
    </router-link>
  </div>
</template>

<style lang="scss" scoped>
.main-menu {
  color: inherit;
  > a {
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 150px;
    height: 100%;
    padding: 0 2rem;
    color: inherit;
    text-decoration: none;
    transition: color, background-color 10ms;
    &:hover {
      color: rgb(var(--c-black));
      background: rgba(var(--c-page-fg), 0.1);
      transition: color, background-color 200ms;
    }
    &.router-link-active {
      //color: rgb(var(--c-page-bg));
      //background: rgb(var(--c-page-fg));
      color: #fff;
      background: black;
      transition: color, background-color 200ms;
    }
  }
}
</style>
