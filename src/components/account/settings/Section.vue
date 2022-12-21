<script lang="ts">
import { computed, defineComponent } from "vue";

import IconEdit from "@/components/ui/icon/IconEdit.vue";

export default defineComponent({
  components: {
    IconEdit,
  },
  props: {
    title: {
      type: String,
      required: false,
      default: null,
    },
    outlined: {
      type: Boolean,
      default: true,
    },
    readonly: {
      type: Boolean,
      default: false,
    },
  },
  setup(props, { attrs, emit }) {
    const isEditable = computed(() => {
      if (props.readonly) {
        return false;
      }
      return !!attrs.onEdit;
    });
    const handleEdit = () => {
      if (!isEditable.value) {
        return;
      }
      emit("edit");
    };
    return {
      isEditable,
      handleEdit,
    };
  },
});
</script>

<template>
  <section
    class="section"
    :class="{
      'is-outlined': outlined,
      'is-readonly': readonly,
      'is-editable': isEditable,
    }"
  >
    <div class="title" v-if="title" v-text="title" />
    <div class="panel" @click="handleEdit">
      <slot name="default" />
      <div v-if="isEditable" class="panel-icon">
        <IconEdit :scale="0.75" />
      </div>
    </div>
  </section>
</template>

<style lang="scss" scoped>
@use "@/style/base/responsive";
@use "@/style/base/typo";

.section {
  margin: 2rem 0;

  .title {
    padding-bottom: 0.4rem;
    @include responsive.bp-medium {
      @include typo.small;

      padding-bottom: 0.6rem;
    }
  }

  &.is-readonly {
    pointer-events: none;
  }

  &.is-outlined {
    .panel {
      min-height: 46px;
      padding: 0.75rem;
      border: 1px solid rgb(var(--c-dark) / 20%);

      [data-theme="dark"] & {
        border-color: rgb(var(--c-dark) / 5%);
        background: rgb(var(--c-dark) / 5%);
      }
    }
  }

  &.is-editable {
    /* stylelint-disable-next-line no-descending-specificity */
    .panel {
      cursor: pointer;
      position: relative;
      transition: background 200ms, border 200ms;

      @include responsive.on-hover {
        background: rgb(var(--c-dark) / 10%);
      }

      .panel-icon {
        top: 0;
        position: absolute;
        right: 0;
      }
    }

    &.is-outlined {
      .panel {
        @include responsive.on-hover {
          border-color: rgb(var(--c-dark) / 1%);
        }
      }
    }
  }
}
</style>
