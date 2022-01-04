<script lang="ts">
import { debounce } from 'lodash-es';
import {
  ref,
  computed,
  defineComponent,
  watch,
  onMounted,
} from 'vue';
import { useStore } from 'vuex';

import notify from '@/utils/notification';

import OverlayPanel from '@/components/ui/panel/OverlayPanel.vue';
import CircleButton from '@/components/ui/button/CircleButton.vue';
import IconHeart from '@/components/ui/icon/IconHeart.vue';
import IconFlash from '@/components/ui/icon/IconFlash.vue';
import RadioInput from '@/components/ui/form/RadioInput.vue';
import TextareaInput from '@/components/ui/form/TextareaInput.vue';

const REASONS = [
  {
    value: 'track',
    label: 'Ich mag diesen Track nicht',
  },
  {
    value: 'emission',
    label: 'Ich mag diese Sendung nicht',
  },
  {
    value: 'daytime',
    label: 'Der Track oder die Sendung passen nicht zur Tageszeit',
  },
  {
    value: 'repetition',
    label: 'Ich habe diesen Track schon zu oft gehört',
  },
];

export default defineComponent({
  props: {
    media: {
      type: Object,
      required: true,
    },
  },
  components: {
    OverlayPanel,
    CircleButton,
    IconHeart,
    IconFlash,
    RadioInput,
    TextareaInput,
  },
  setup(props) {
    const store = useStore();
    const objKey = computed(() => {
      return `${props.media.ct}:${props.media.uid}`;
    });
    const userRating = computed(() => {
      return store.getters['rating/ratingByKey'](objKey.value);
    });
    const userRatingValue = computed(() => {
      return userRating.value?.value;
    });
    const promptVisible = ref(false);
    const scopes = computed(() => REASONS);
    const scope = ref('track');
    const comment = ref('');
    const showPrompt = () => {
      promptVisible.value = true;
    };
    const hidePrompt = () => {
      comment.value = '';
      promptVisible.value = false;
    };
    const rate = debounce(async (value: number) => {
      const vote = {
        key: objKey.value,
        value: userRatingValue.value === value ? null : value,
      };
      if (vote.value === -1) {
        showPrompt();
      } else {
        await store.dispatch('rating/updateRating', vote);
      }
    }, 200);
    const downvote = async () => {
      const vote = {
        key: objKey.value,
        value: -1,
        scope: scope.value,
        comment: comment.value,
      };
      hidePrompt();
      await store.dispatch('rating/updateRating', vote);
      notify({
        level: 'success',
        ttl: 5,
        body: 'Vielen Dank für dein feedback!',
      });
    };
    const fetchRating = async (key: string) => {
      if (!key) {
        return;
      }
      if (userRating.value) {
        return;
      }
      await store.dispatch('rating/loadRating', key);
    };
    onMounted(() => {
      fetchRating(objKey.value);
    });
    watch(objKey, async (key) => {
      await fetchRating(key);
    });
    return {
      userRating,
      userRatingValue,
      rate,
      promptVisible,
      scopes,
      scope,
      comment,
      hidePrompt,
      downvote,
    };
  },
});
</script>

<template>
  <div
    class="rating"
  >
    <div
      class="total"
    >
      ?
    </div>
    <div>
      <CircleButton
        :size="48"
        @click="rate(1)"
      >
        <IconHeart
          :size="48"
          :outlined="(userRatingValue !== 1)"
          color="rgb(var(--c-page-fg))"
        />
      </CircleButton>
    </div>
    <div>
      <CircleButton
        :size="48"
        @click="rate(-1)"
      >
        <IconFlash
          :size="48"
          :outlined="(userRatingValue !== -1)"
          color="rgb(var(--c-page-fg))"
        />
      </CircleButton>
    </div>
    <div
      class="total"
    >
      ?
    </div>
  </div>
  <OverlayPanel
    :is-visible="promptVisible"
    @close="hidePrompt"
    title="Was stört dich?"
  >
    <div
      class="prompt"
    >
      <div
        class="prompt__lead"
      >
        <p>Um das Radioprogramm ständig zu verbessern benötigen wir dein Feedback!</p>
      </div>
      <div
        class="prompt__scopes"
      >
        <RadioInput
          v-for="s in scopes"
          v-model="scope"
          name="scope"
          :key="`scope-${s.value}`"
          :value="s.value"
          :label="s.label"
          class="scope"
        />
      </div>
      <div
        class="prompt__comment"
      >
        <TextareaInput
          v-model="comment"
          :maxlength="(256)"
          label="Kommentar"
        />
      </div>
      <div
        class="prompt__actions"
      >
        <button
          class="button"
          @click="downvote"
        >
          Senden
        </button>
      </div>
    </div>
    <template
      #footer
    >
      <div>(( footer content ))</div>
    </template>
  </OverlayPanel>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/elements/button";
.rating {
  display: grid;
  grid-template-columns: repeat(4, 4rem);
  > div {
    align-self: center;
    justify-self: center;
  }
  .total {
    @include typo.dim;
    @include typo.light;
    opacity: 0;
  }
}
.prompt {
  &__lead {
    padding: 0 0 1rem;
    @include typo.large;
  }
  &__scopes {
    padding: 1rem 0;
  }
  &__comment {
    padding: 1rem 0;
    textarea {
      @include typo.large;
      width: 100%;
      min-height: 4rem;
      padding: 0.54rem;
    }
  }
  &__actions {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    padding: 1rem 0;
    .button {
      @include button.default(3rem);
      min-width: 33%;
    }
  }
}
</style>
