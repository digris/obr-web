<script lang="ts">
import { ref, computed, defineComponent, watch, onMounted } from "vue";
import { useI18n } from "vue-i18n";
import { debounce } from "lodash-es";

import OverlayPanel from "@/components/ui/panel/OverlayPanel.vue";
import CircleButton from "@/components/ui/button/CircleButton.vue";
import IconHeart from "@/components/ui/icon/IconHeart.vue";
import IconFlash from "@/components/ui/icon/IconFlash.vue";
import RadioInput from "@/components/ui/form/RadioInput.vue";
import TextareaInput from "@/components/ui/form/TextareaInput.vue";
import { useRatingStore } from "@/stores/rating";
import { useNotification } from "@/composables/notification";

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
    const { t } = useI18n();
    const objKey = computed(() => `${props.media.ct}:${props.media.uid}`);
    const { ratingByKey, loadRating, setRating } = useRatingStore();
    const { notify } = useNotification();
    const rating = computed(() => ratingByKey(objKey.value));
    const promptVisible = ref(false);
    const scope = ref("track");
    const comment = ref("");
    const showPrompt = () => {
      promptVisible.value = true;
    };
    const hidePrompt = () => {
      comment.value = "";
      promptVisible.value = false;
    };
    const isFlipped = ref(0);
    const flipIcon = async (value: number) => {
      isFlipped.value = value;
      return new Promise<void>((resolve) => {
        setTimeout(() => {
          isFlipped.value = 0;
          resolve();
        }, 200);
      });
    };
    const rate = debounce(
      async (value: number) => {
        if (value === -1) {
          showPrompt();
          await flipIcon(value);
        } else {
          await setRating(objKey.value, value);
        }
      },
      200,
      { leading: true, trailing: false }
    );
    const downvoteScopes = computed(() => {
      return [
        {
          value: "track",
          label: t("rating.downvoteScope.track"),
        },
        {
          value: "genre",
          label: t("rating.downvoteScope.genre"),
        },
        {
          value: "emission",
          label: t("rating.downvoteScope.emission"),
        },
        {
          value: "daytime",
          label: t("rating.downvoteScope.daytime"),
        },
        {
          value: "repetition",
          label: t("rating.downvoteScope.repetition"),
        },
      ];
    });
    const downvote = async () => {
      hidePrompt();
      await setRating(objKey.value, -1, {
        scope: scope.value,
        comment: comment.value,
      });
      /**/
      await notify({
        level: "success",
        ttl: 5,
        body: t("rating.downvoteThankYou"),
      });
    };
    onMounted(async () => {
      if (rating.value === undefined) {
        await loadRating(objKey.value);
      }
    });
    watch(objKey, async (key) => {
      await loadRating(key);
    });
    return {
      t,
      rating,
      rate,
      isFlipped,
      promptVisible,
      downvoteScopes,
      scope,
      comment,
      hidePrompt,
      downvote,
    };
  },
});
</script>

<template>
  <div class="rating">
    <div class="total">?</div>
    <div>
      <CircleButton @click="rate(rating === 1 ? null : 1)" :outlined="true">
        <div
          class="flip-container"
          :class="{
            'is-flipped': isFlipped === 1,
          }"
        >
          <IconHeart :outlined="rating !== 1" color-var="--c-page-fg" />
        </div>
      </CircleButton>
    </div>
    <div>
      <CircleButton @click="rate(rating === -1 ? null : -1)" :outlined="true">
        <div
          class="flip-container"
          :class="{
            'is-flipped': isFlipped === -1,
          }"
        >
          <IconFlash :outlined="rating !== -1" color-var="--c-page-fg" />
        </div>
      </CircleButton>
    </div>
    <div class="total">?</div>
  </div>
  <OverlayPanel :is-visible="promptVisible" @close="hidePrompt" :title="t('rating.downvoteTitle')">
    <div class="prompt">
      <div class="prompt__lead">
        <p v-text="t('rating.downvoteLead')" />
      </div>
      <div class="prompt__scopes">
        <RadioInput
          v-for="s in downvoteScopes"
          v-model="scope"
          name="scope"
          :key="`scope-${s.value}`"
          :value="s.value"
          :label="s.label"
          class="scope"
        />
      </div>
      <div class="prompt__comment">
        <TextareaInput v-model="comment" :maxlength="256" :label="t('rating.downvoteComment')" />
      </div>
      <div class="prompt__actions">
        <button class="button" @click="downvote" v-text="t('formActions.send')" />
      </div>
    </div>
  </OverlayPanel>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
@use "@/style/abstracts/responsive";
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
  .flip-container {
    width: 100%;
    height: 100%;
    transition: opacity 200ms ease-in-out, transform 200ms ease-in;
    &.is-flipped {
      transform: rotateY(89deg);
    }
  }
  @include responsive.bp-medium {
    grid-template-columns: auto 52px 52px auto;
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
