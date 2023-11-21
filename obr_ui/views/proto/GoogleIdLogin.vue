<script lang="ts" setup>
import { onMounted } from "vue";

const appBridge = window.appBridge;

onMounted(() => {
  console.debug("mounted");
});

const startLogin = async () => {
  console.debug("start login");
  if (appBridge) {
    await appBridge.send("googleSignin:start");
  }
};
</script>

<template>
  <div class="container">
    <div class="actions">
      <button @click="startLogin()">Start Google Login</button>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  padding: 2rem;
  .actions {
    button {
      height: 24px;
      max-width: 200px;
    }
  }
}
</style>
