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
import Datetime from '@/components/ui/date/Datetime.vue';

export default defineComponent({
  components: {
    AsyncButton,
    APIErrors,
    Datetime,
  },
  emits: [
    'subscriptionCreated',
  ],
  setup(props, { emit }) {
    const store = useStore();
    const isSuccess = ref(false);
    const errors = ref<Array<string>>([]);
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
        emit('subscriptionCreated');
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
        <div
          v-if="firstOption"
          class="option"
        >
          <span>
            Your {{ firstOption.numDays }} day Trial
          </span>
          <span>
            until
            <Datetime
              :display-time="(false)"
              :value="firstOption.untilDate"
            />
          </span>
        </div>
        <p
          class="message"
          v-text="message"
        />
      </div>
    </section>
    <section
      v-if="errors.length"
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
  padding: 2rem 0 1rem;
  text-align: center;
  &.info {
    .option {
      display: flex;
      flex-direction: column;
      font-size: 3rem;
      text-align: center;
    }
    .message {
      padding: 1rem 0;
      font-size: 1.75rem;
      line-height: 130%;
    }
  }
  &.actions {
    display: flex;
    align-items: center;
    justify-content: center;
  }
}
.button {
  @include button.default(4rem);
}
</style>
