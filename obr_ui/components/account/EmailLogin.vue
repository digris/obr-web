<script lang="ts">
import { defineComponent, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

import IconBuffering from "@/components/ui/icon/IconBuffering.vue";
import { useAccount } from "@/composables/account";
import Page from "@/layouts/Page.vue";

export default defineComponent({
  components: {
    Page,
    IconBuffering,
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const { loginUserBySignedEmail } = useAccount();
    const { loadUser } = useAccount();
    const signedEmail = ref(route.params.signedEmail);
    const errors = ref<Array<string>>([]);
    const loginBySignedEmail = async (value: string | string[]) => {
      try {
        await loginUserBySignedEmail(value);
        await loadUser();
        // document.location.href = "/account/settings/";
        await router.push("/account/settings/");
      } catch (err) {
        console.warn(err);
        errors.value = [err.message, err.response.data];
      }
    };
    if (signedEmail.value) {
      loginBySignedEmail(signedEmail.value);
    }
    return {
      errors,
      signedEmail,
    };
  },
});
</script>
<template>
  <Page class="email-login" title="Login">
    <div class="loading">
      <IconBuffering />
      <div class="text">loading user data</div>
    </div>
    <div class="errors" v-if="errors.length">
      <pre v-text="errors" />
    </div>
  </Page>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/base/responsive";
@use "@/style/elements/form";

.email-login {
  flex-grow: 1;
  display: flex;
  flex-direction: column;

  .loading {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding-bottom: 6rem;

    > .text {
      @include typo.small;
    }
  }

  .errors {
    display: none;
  }
}
</style>
