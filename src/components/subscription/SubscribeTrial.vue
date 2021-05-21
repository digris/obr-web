<script lang="ts">
import {
  computed,
  defineComponent,
  onMounted,
  ref,
} from 'vue';
import { useStore } from 'vuex';
import AsyncButton from '@/components/ui/button/AsyncButton.vue';
import APIErrors from '@/components/ui/error/APIErrors.vue';

import { startTrial, getTrialOptions } from '@/api/subscription';
import Datetime from '@/components/ui/Datetime.vue';

export default defineComponent({
  components: {
    AsyncButton,
    APIErrors,
    Datetime,
  },
  setup() {
    const store = useStore();
    const isSuccess = ref(false);
    const errors = ref<Array<String>>([]);
    const message = ref(null);
    const options = ref([]);
    const fetchOptions = async () => {
      errors.value = [];
      try {
        const response = await getTrialOptions();
        message.value = response.message;
        options.value = response.options;
      } catch (err: any) {
        errors.value = [err.response];
      }
    };
    // eslint-disable-next-line arrow-body-style
    const firstOption = computed(() => {
      return (options.value.length) ? options.value[0] : null;
    });
    const start = async () => {
      errors.value = [];
      try {
        console.debug('asdasd');
        const response = await startTrial();
        console.debug(response);
        await store.dispatch('account/getUser');
        isSuccess.value = true;
        // close();
      } catch (err: any) {
        console.warn(err);
        // errors.value = [err.message, err.response.data];
        errors.value = [err.response];
        throw err;
      }
    };
    onMounted(() => {
      fetchOptions();
    });
    return {
      message,
      options,
      firstOption,
      isSuccess,
      errors,
      start,
    };
  },
});
</script>

<template>
  <div
    class="subscribe-trial"
  >
    <section
      class="section info"
    >
      <div>
        <p
          class="message"
          v-text="message"
        />
        <div
          v-if="firstOption"
          class="details"
        >
          <span>
            Full acces for {{ firstOption.numDays }} days
          </span>
          <span>
            <span> &bull; </span>
            until
            <Datetime
              :display-time="(false)"
              :value="firstOption.untilDate"
            />
          </span>
        </div>
      </div>
    </section>
    <section
      v-if="errors"
      class="section errors"
    >
      <APIErrors
        :errors="errors"
      />
    </section>
    <section
      class="section actions"
    >
      <AsyncButton
        class="button"
        @click.prevent="start"
      >
        Start trial now
      </AsyncButton>
    </section>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/elements/section";
@use "@/style/elements/button";
.section {
  @include section.default;
  &.info {
    .message {
      padding: 1rem 0;
    }
    .details {
      font-size: 150%;
    }
  }
}
.button {
  @include button.default;
}
</style>
