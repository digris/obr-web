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
  },
  setup(props, { attrs, emit }) {
    const isEditable = computed(() => {
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
@use "@/style/abstracts/responsive";
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
  /*
  .panel {
    padding-top: 0.75rem;
  }
  */
  &.is-outlined {
    .panel {
      min-height: 46px;
      padding: 0.75rem;
      border: 1px solid rgb(var(--c-gray-200));
    }
  }
  &.is-editable {
    .panel {
      cursor: pointer;
      position: relative;
      &:hover {
        background: rgba(var(--c-black), 0.1);
      }
      .panel-icon {
        position: absolute;
        right: 0;
        top: 0;
      }
    }
  }
}
</style>
