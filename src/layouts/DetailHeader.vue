<script lang="ts">
import {
  defineComponent,
  ref,
  onMounted, computed,
} from 'vue';
import { useRouter } from 'vue-router';

import BackButton from '@/components/ui/button/BackButton.vue';
import CircleButton from '@/components/ui/button/CircleButton.vue';
import UserRating from '@/components/rating/UserRating.vue';
import ContextMenu from '@/components/context-menu/ContextMenu.vue';

export default defineComponent({
  components: {
    BackButton,
    CircleButton,
    UserRating,
    ContextMenu,
  },
  props: {
    // objKey: {
    //   type: String,
    //   required: true,
    // },
    obj: {
      type: Object,
      required: true,
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
    showContextMenu: {
      type: Boolean,
      default: true,
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
  <div
    class="detail-header"
  >
    <div
      class="top"
    >
      <div
        class="back"
      >
        <BackButton
          v-if="canNavigateBack"
          @click="back"
        />
        <div
          class="scope"
          v-if="titleScope"
          v-text="titleScope"
        />
      </div>
      <div
        class="title"
      />
      <div
        class="actions"
      >
        <CircleButton
          v-if="showContextMenu"
          :size="(48)"
          :outlined="(false)"
        >
          <UserRating
            :obj-key="objKey"
            :autoload="(true)"
          />
        </CircleButton>
        <ContextMenu
          v-if="showContextMenu"
          :obj="obj"
        />
      </div>
    </div>
    <div
      class="main"
    >
      <div
        class="visual"
      >
        <slot
          name="visual"
        />
      </div>
      <div
        class="body"
      >
        <div
          class="title"
        >
          <!--
          <div
            class="title--scope"
            v-if="titleScope"
            v-text="titleScope"
          />
          -->
          <h1
            class="title--primary"
            v-text="title"
          />
        </div>
        <slot
          name="info-panel"
        />
      </div>
    </div>
    <div
      class="bottom"
    >
      <div
        class="meta"
      >
        <slot
          name="meta-panel"
        />
      </div>
      <div
        class="searchbar"
      >
        <slot
          name="searchbar"
        />
      </div>
    </div>
    <div
      class="background"
    >
      <slot
        name="background"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
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
    position: sticky;
    top: 0;
    z-index: 4;
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    height: 4rem;
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
      padding-left: 4rem;
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
      :deep(.image) {
        @include visual-image;
      }
    }
    .body {
      position: absolute;
      top: 0;
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
  .background {
    position: absolute;
    z-index: 2;
    width: 100%;
    height: 100%;
  }
}
</style>
