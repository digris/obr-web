<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";
import { useRouter } from "vue-router";

import BackButton from "@/components/ui/button/BackButton.vue";

export default defineComponent({
  components: {
    BackButton,
  },
  props: {
    titleScope: {
      type: String,
      required: false,
      default: null,
    },
  },
  setup() {
    const router = useRouter();
    const canNavigateBack = ref(false);
    const back = () => {
      if (canNavigateBack.value) {
        router.back();
      }
    };
    onMounted(() => {
      if (window?.history?.length > 2) {
        canNavigateBack.value = true;
      }
    });
    return {
      canNavigateBack,
      back,
    };
  },
});
</script>

<template>
  <div class="detail-header">
    <div class="top">
      <div class="back">
        <BackButton v-if="canNavigateBack" @click="back" />
      </div>
      <div class="scope">
        <span v-if="titleScope" v-text="`${titleScope}:`" />
      </div>
    </div>
    <div class="main">
      <div class="visual">
        <div class="image" />
      </div>
      <div class="body">
        <div class="title">
          <h1 class="title--primary" />
        </div>
      </div>
    </div>
    <div class="bottom">
      <div class="meta" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/responsive";
@use "@/style/base/typo";
@use "@/style/elements/container";
@mixin visual-image {
  height: 50vh;
  min-height: 280px;
  max-height: 620px;

  .image {
    height: 100%;
  }

  img {
    border-radius: 50%;
  }
}

.detail-header {
  position: relative;
  display: flex;
  flex-direction: column;

  .top,
  .main,
  .bottom,
  .appendix {
    @include container.default;

    z-index: 3;
  }

  .top {
    top: 0;
    position: sticky;
    height: 4rem;
    z-index: 4;
    display: grid;
    grid-template-columns: 64px auto 1fr;
    align-items: center;
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;

    > .back {
      display: flex;
      align-items: center;

      .scope {
        padding-left: 1rem;
      }
    }

    > .actions {
      display: flex;
      justify-self: flex-end;
    }
  }

  .bottom {
    display: grid;
    grid-template-columns: auto 1fr;
    align-items: center;
    height: 3rem;
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;

    .meta {
      padding-left: 1rem;
    }

    > .filterbar {
      background: transparent;
    }
  }

  .main {
    position: relative;
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    justify-content: center;

    .visual {
      display: flex;
      align-items: center;
      justify-content: center;

      .image {
        @include visual-image;

        height: 50vh;
        min-height: 280px;
        max-height: 620px;
        background: rgb(var(--c-white) 0.1);
        aspect-ratio: 1;
        border-radius: 50%;
      }
    }

    .body {
      top: 0;
      position: absolute;
      width: calc(50% - 48px); // TODO: width calculation
      margin-top: -1.5rem;
      padding-left: calc(48px + 1rem);

      .title {
        margin-bottom: 0.5rem;

        /*
        &--scope {
          @include typo.default;
          @include typo.bold;
          line-height: 1.5rem;
        }
        */
        &--primary {
          @include typo.x-large;
          @include typo.bold;

          line-height: 4rem;
        }
      }
    }
  }
  @include responsive.bp-medium {
    .top {
      grid-template-columns: 80px auto 80px;
      margin: 0;
      height: 60px;

      .scope {
        display: flex;
        justify-content: center;
      }
    }

    .main {
      align-items: center;

      .visual {
        width: 73%;
        aspect-ratio: 1;

        .image {
          height: unset;
          aspect-ratio: 1;
        }
      }
    }
  }
}
</style>
