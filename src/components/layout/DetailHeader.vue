<script lang="ts">
import {
  defineComponent,
  ref,
  onMounted,
} from 'vue';
import { useRouter } from 'vue-router';

import BackButton from '@/components/ui/button/BackButton.vue';
import UserRating from '@/components/rating/UserRating.vue';

export default defineComponent({
  components: {
    BackButton,
    UserRating,
  },
  props: {
    // scope: {
    //   type: String,
    //   required: false,
    //   default: null,
    // },
    objKey: {
      type: String,
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
    enableRating: {
      type: Boolean,
      default: false,
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
      </div>
      <div
        class="title"
      />
      <div
        class="actions"
      >
        <UserRating
          v-if="enableRating"
          :obj-key="objKey"
          :autoload="(true)"
        />
      </div>
    </div>
    <div
      class="main"
    >
      <div
        class="t-visual"
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
          <div
            class="title--scope"
            v-if="titleScope"
            v-text="titleScope"
          />
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
        class="noop"
      >

      </div>
      <div
        class="meta"
      >
        <slot
          name="meta-panel"
        />
      </div>
      <div
        class="actions"
      >
        ...
      </div>
    </div>
    <div
      class="appendix"
    >
      <slot
        name="appendix"
      />
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
@mixin visual {
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
    top: 78px;
  }
  .top,
  .bottom {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    height: 4rem;
    padding-top: 1rem;
    padding-bottom: 1rem;
    .actions {
      justify-self: flex-end;
    }
  }
  .main {
    position: relative;
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    justify-content: center;
    .t-visual {
      display: flex;
      align-items: center;
      justify-content: center;
      :deep(.visual) {
        @include visual;
      }
    }
    .body {
      position: absolute;
      top: 0;
      .title {
        margin-bottom: 0.5rem;
        &--scope {
          @include typo.default;
          @include typo.bold;
          line-height: 1.5rem;
        }
        &--primary {
          @include typo.x-large;
          @include typo.bold;
          line-height: 4rem;
        }
      }
    }
  }
  .appendix {
    display: flex;
  }
  .background {
    position: absolute;
    z-index: 2;
    width: 100%;
    height: 100%;
  }
}
</style>
