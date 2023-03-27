<script lang="ts" setup>
import { ref, watch } from "vue";
import { debounce } from "lodash-es";

const email = ref("");
const handleEmailChanged = debounce(async (e: any) => {
  console.debug("handleEmailInput", e);
});
watch(() => email.value, handleEmailChanged);
</script>

<template>
  <div>
    <div class="container">
      <div class="autocomplete">
        <input
          v-model="email"
          name="email"
          type="email"
          placeholder="E-Mail"
          autocomplete="email"
        />
      </div>
      <div>
        <pre
          class="debug"
          v-text="{
            email,
          }"
        />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.container {
  padding: 1rem;
  > .autocomplete {
    background: yellow;
    > input {
      width: 100%;
      height: 30px;
    }
  }
}
</style>
