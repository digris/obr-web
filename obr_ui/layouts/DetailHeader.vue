<script lang="ts">
import { computed, defineComponent, onMounted, ref } from "vue";
import { useRouter } from "vue-router";

import ContextMenu from "@/components/context-menu/ContextMenu.vue";
import UserRating from "@/components/rating/UserRating.vue";
import BackButton from "@/components/ui/button/BackButton.vue";
import CircleButton from "@/components/ui/button/CircleButton.vue";

export default defineComponent({
  components: {
    BackButton,
    CircleButton,
    UserRating,
    ContextMenu,
  },
  props: {
    obj: {
      type: Object,
      required: true,
    },
    layout: {
      type: String,
      default: "circle",
    },
    titleScope: {
      type: String,
      required: false,
      default: null,
    },
    title: {
      type: String,
      required: false,
      default: null,
    },
    showObjRating: {
      type: Boolean,
      default: true,
    },
    showContextMenu: {
      type: Boolean,
      default: true,
    },
    mobileBodyPosition: {
      type: String,
      default: "bottom",
    },
  },
  setup(props) {
    const router = useRouter();
    const objKey = computed(() => `${props.obj.ct}:${props.obj.uid}`);
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
      objKey,
      canNavigateBack,
      back,
    };
  },
});
</script>

<template>
  <div class="detail-header" :class="`layout-${layout}`">
    <div class="top">
      <div class="back">
        <BackButton v-if="canNavigateBack" @click="back" />
      </div>
      <div class="scope">
        <span v-if="titleScope" v-text="`${titleScope}:`" />
      </div>
      <div class="actions">
        <CircleButton v-if="showObjRating">
          <UserRating :obj-key="objKey" :autoload="true" />
        </CircleButton>
        <ContextMenu v-if="showContextMenu" :obj="obj" />
      </div>
    </div>
    <div class="main">
      <div class="visual">
        <slot name="visual" />
      </div>
      <div class="body" :class="`mobile-position--${mobileBodyPosition}`">
        <div class="title">
          <h1 class="title--primary" v-text="title" />
        </div>
        <div class="info-panel">
          <slot name="info-panel" />
        </div>
      </div>
    </div>
    <div class="bottom">
      <div class="meta">
        <slot name="meta-panel" />
      </div>
      <div class="searchbar">
        <slot name="searchbar" />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/style/base/responsive";
@use "@/style/base/typo";
@use "@/style/elements/container";

@mixin visual-circle {
  height: 50vh;
  min-height: 280px;
  max-height: 620px;

  .image {
    height: 100%;
  }

  img {
    border-radius: 50%;
  }

  @include responsive.bp-medium {
    height: unset;
  }
}

@mixin visual-square {
  height: 50vh;
  min-height: 280px;
  max-height: 620px;
  background: rgb(var(--c-page-bg) / 100%);

  .image {
    height: 100%;
  }

  img {
    filter: grayscale(100%) brightness(125%);
    mix-blend-mode: multiply;
  }

  @include responsive.bp-medium {
    height: unset;
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

      .placeholder {
        width: 48px;
      }

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
      padding-left: 0;
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

    .body {
      top: 0;
      position: absolute;
      width: calc(50% - 48px); // TODO: width calculation
      margin-top: -1.5rem;
      padding-left: calc(48px + 1rem);

      .title {
        margin-bottom: 0.5rem;

        &--primary {
          @include typo.x-large;

          line-height: 4rem;
        }
      }
    }
  }

  &.layout-circle {
    .visual {
      display: flex;
      align-items: center;
      justify-content: center;

      :deep(.image) {
        @include visual-circle;
      }
    }
  }

  &.layout-square {
    .visual {
      display: flex;
      align-items: center;
      justify-content: flex-start;
      padding-left: 50%;

      :deep(.image) {
        @include visual-square;
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
        width: 73%; // NOTE: check calculation
        aspect-ratio: 1;

        .image {
          aspect-ratio: 1;
        }
      }

      .body {
        position: relative;
        width: unset;
        padding: 1rem 0 0;
        text-align: center;
        margin-top: unset;

        .title {
          margin-bottom: 0;

          &--primary {
            @include typo.large;

            line-height: unset;
          }
        }

        /*
          NOTE: ugly hack here: in a single case ("mood") we have to move the body / title
                to the top...
        */
        &.mobile-position {
          &--top {
            top: -1rem;
            position: absolute;
            padding: 0;

            .title {
              &--primary {
                @include typo.x-large;
              }
            }
          }
        }

        .info-panel {
          @include typo.light;

          margin-bottom: 1rem;

          :deep(div) {
            margin: 0; // NOTE: do we really want this?
          }

          :deep(.identifiers),
          :deep(.editor) {
            margin-top: 1.5rem;
            margin-bottom: 0.5rem;
          }
        }

        :deep(a) {
          text-decoration: underline;
        }
      }
    }

    &.layout-square {
      .visual {
        padding-left: unset;
      }
    }
  }
}
</style>
