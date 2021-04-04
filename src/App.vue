<script>
import { AudioPlayer } from '@/player/audioPlayer';
import Player from '@/components/player/Player.vue';
import ColorChooser from '@/components/colors/ColorChooser.vue';

export default {
  components: {
    Player,
    // debug
    ColorChooser,
  },
  created() {
    this.audioPlayer = new AudioPlayer();
  },
};
</script>

<template>
  <div class="topbar">
    <div class="brand">
      open broadcast
    </div>
    <div class="menu menu--main">
      <router-link to="/">On Air</router-link>
      <router-link to="/discover/">Discover</router-link>
      <router-link to="/collection/">My Likes</router-link>
    </div>
    <div class="menu menu--account">
      <router-link to="/account/">Peter</router-link>
    </div>
    <div class="menu-toggle">
      +
    </div>
  </div>
  <router-view v-slot="{ Component }">
    <keep-alive>
      <component :is="Component" />
    </keep-alive>
  </router-view>
  <ColorChooser />
  <Player />
</template>

<style lang="scss">
.topbar {
  position: sticky;
  top: 0;
  display: grid;
  grid-template-columns: 180px 1fr 120px 40px;
  height: 48px;
  //background: rgba(50,50,50,0.2);
  background: rgba(var(--c-live-bg), 0.9);
  transition: background 3000ms;
  backdrop-filter: blur(2px);
  z-index: 2;
  .brand {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    padding-left: 1rem;
  }
  .menu {
    display: flex;
    align-items: center;
    &--main {
      justify-content: center;
    }
    &--account {
      justify-content: flex-end;
    }
  }
  .menu-toggle {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding: 0 1rem;
  }
  .menu {
    color: inherit;
    > a {
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 0 2rem;
      height: 100%;
      color: inherit;
      text-decoration: none;
      transition: color, background-color 200ms;
      &:hover,
      &.router-link-active {
        color: #fff;
        background: black;
      }
    }
  }
}
</style>
