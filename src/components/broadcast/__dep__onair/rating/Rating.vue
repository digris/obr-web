<script lang="ts">
import { ref, computed, defineComponent, watch, onMounted } from "vue";
import { useStore } from "vuex";
import { useI18n } from "vue-i18n";
import { debounce } from "lodash-es";

import OverlayPanel from "@/components/ui/panel/OverlayPanel.vue";
import CircleButton from "@/components/ui/button/CircleButton.vue";
import IconHeart from "@/components/ui/icon/IconHeart.vue";
import IconFlash from "@/components/ui/icon/IconFlash.vue";
import RadioInput from "@/components/ui/form/RadioInput.vue";
import TextareaInput from "@/components/ui/form/TextareaInput.vue";

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
    const store = useStore();
    const objKey = computed(() => {
      return `${props.media.ct}:${props.media.uid}`;
    });
    const userRating = computed(() => {
      return store.getters["rating/ratingByKey"](objKey.value);
    });
    const userRatingValue = computed(() => {
      return userRating.value?.value;
    });
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
        await flipIcon(value);
        const vote = {
          key: objKey.value,
          value: userRatingValue.value === value ? null : value,
        };
        if (vote.value === -1) {
          showPrompt();
        } else {
          await store.dispatch("rating/updateRating", vote);
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
          label: "Ich mag diese Art von Musik nicht",
        },
        {
          value: "emission",
          label: "Ich mag diese Sendung nicht",
        },
        {
          value: "daytime",
          label: "Der Track oder die Sendung passen nicht zur Tageszeit",
        },
        {
          value: "repetition",
          label: "Ich habe diesen Track schon zu oft gehört",
        },
      ];
    });
    const downvote = async () => {
      const vote = {
        key: objKey.value,
        value: -1,
        scope: scope.value,
        comment: comment.value,
      };
      hidePrompt();
      await store.dispatch("rating/updateRating", vote);
    };
    const fetchRating = async (key: string) => {
      if (!key) {
        return;
      }
      if (userRating.value) {
        return;
      }
      await store.dispatch("rating/loadRating", key);
    };
    onMounted(() => {
      fetchRating(objKey.value);
    });
    watch(objKey, async (key) => {
      await fetchRating(key);
    });
    return {
      t,
      userRating,
      userRatingValue,
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
      <CircleButton @click="rate(1)" :outlined="true">
        <div
          class="flip-container"
          :class="{
            'is-flipped': isFlipped === 1,
          }"
        >
          <IconHeart :outlined="userRatingValue !== 1" color-var="--c-page-fg" />
        </div>
      </CircleButton>
    </div>
    <div>
      <CircleButton @click="rate(-1)" :outlined="true">
        <div
          class="flip-container"
          :class="{
            'is-flipped': isFlipped === -1,
          }"
        >
          <IconFlash :outlined="userRatingValue !== -1" color-var="--c-page-fg" />
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
        <TextareaInput v-model="comment" :maxlength="256" label="Kommentar" />
      </div>
      <div class="prompt__actions">
        <button class="button" @click="downvote">Senden</button>
      </div>
    </div>
    <template #footer>
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
  .flip-container {
    width: 100%;
    height: 100%;
    transition: opacity 200ms ease-in-out, transform 200ms ease-in;
    &.is-flipped {
      transform: rotateY(89deg);
    }
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
