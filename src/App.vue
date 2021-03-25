<template>
  <p>...</p>
  <Player msg="Hi!"/>
</template>

<script>
import Player from './components/Player.vue';

export default {
  name: 'App',
  components: {
    Player,
  },
};
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #333333;
  margin-top: 60px;
}
pre {
  &.debug {
    padding: 1rem;
    background: #222;
    color: #FFFFFF;
  }
}
</style>
