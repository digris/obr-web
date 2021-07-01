<template>
  <div
    class="main-menu"
  >
    <router-link
      to="/"
    >
      On Air
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
    transition: color, background-color 500ms;
    &:hover {
      color: rgb(var(--c-black));
      background: rgba(var(--c-live-fg), 0.2);
      transition: color, background-color 200ms;
    }
    &.router-link-active {
      //color: rgb(var(--c-live-bg));
      //background: rgb(var(--c-live-fg));
      color: #fff;
      background: black;
      transition: color, background-color 200ms;
    }
  }
}
</style>
