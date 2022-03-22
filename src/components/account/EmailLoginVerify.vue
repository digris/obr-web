<script lang="ts">
import { defineComponent, ref } from "vue";
import { useStore } from "vuex";

import AsyncButton from "@/components/ui/button/AsyncButton.vue";
import APIErrors from "@/components/ui/error/APIErrors.vue";
import TokenInput from "@/components/account/TokenInput.vue";

const tokenRegex = new RegExp("^([A-Z0-9]{3})-?([A-Z0-9]{3})$");

export default defineComponent({
  components: {
    AsyncButton,
    APIErrors,
    TokenInput,
  },
  props: {
    email: {
      type: String,
      required: false,
      default: "",
    },
  },
  emits: ["reset"],
  setup(props, { emit }) {
    const store = useStore();
    const token = ref("");
    const tokenValid = ref(false);
    const errors = ref<Array<string>>([]);

    const handleTokenInput = async (value: string) => {
      token.value = value;
      tokenValid.value = tokenRegex.test(value);
      errors.value = [];
      console.debug("value", value);
    };

    const submitForm = async () => {
      console.debug("submit form");
      if (!tokenValid.value) {
        return;
      }
      errors.value = [];
      const credentials = {
        email: props.email,
        token: token.value,
      };
      try {
        await store.dispatch("account/loginUserByToken", credentials);
        await store.dispatch("account/getUser");
        document.location.reload();
      } catch (err) {
        console.warn(err);
        errors.value = [err.response];
        throw err;
      }
    };

    const reset = async () => {
      emit("reset");
    };

    return {
      token,
      tokenValid,
      errors,
      handleTokenInput,
      submitForm,
      reset,
    };
  },
});
</script>

<template>
  <div>
    <p class="lead">
      Eine E-Mail mit einem Login-Code wurde an {{ email }} geschickt.<br />
      Falls du keine E-Mail erhalten hast, prüfe deinen Spam Ordner.<br />
      <a @click.prevent="reset">E-Mail erneut senden</a>
    </p>
  </div>
  <form class="form" @submit.prevent="submitForm">
    <TokenInput ref="tokenInputRef" @input="handleTokenInput" />
    <div class="form-errors" v-if="errors.length">
      <APIErrors :errors="errors" />
    </div>
    <div class="input-container submit">
      <AsyncButton class="button" @click.prevent="submitForm" :disabled="!tokenValid">
        Anmelden
      </AsyncButton>
    </div>
  </form>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/elements/form";
.form {
  @include form.default;
  display: flex;
  flex-direction: column;
  .input-container {
    width: 100%;
    .input {
      @include typo.large;
    }
    &.submit {
      padding-top: 2rem;
      .button {
        max-width: 33%;
      }
    }
  }
  .token-input {
    display: flex;
    flex-direction: column;
    //align-items: center;
    //justify-content: center;
    padding: 1rem 0;
  }
}
.lead {
  @include typo.large;
  a {
    text-decoration: underline;
    cursor: pointer;
  }
}
.form-messages,
.form-errors {
  margin: 1rem 0;
}
</style>
