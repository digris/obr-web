<script lang="ts">
import { computed, defineComponent } from 'vue';

import IconEdit from '@/components/ui/icon/IconEdit.vue';

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
    console.dir(attrs.onEdit);
    const isEditable = computed(() => {
      return !!attrs.onEdit;
    });
    const handleEdit = () => {
      if (!isEditable.value) {
        return;
      }
      emit('edit');
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
    <div
      class="title"
      v-if="title"
      v-text="title"
    />
    <div
      class="panel"
      @click="handleEdit"
    >
      <slot
        name="default"
      />
      <div
        v-if="isEditable"
        class="panel-icon"
      >
        <IconEdit
          :size="48"
        />
      </div>
    </div>
  </section>
</template>

<style lang="scss" scoped>
@use "@/style/base/typo";
.section {
  margin: 2rem 0;
  .title {
    padding-bottom: 0.4rem;
  }
  .panel {
    padding-top: 0.75rem;
    border-radius: 3px;
  }
  &.is-outlined {
    .panel {
      padding: 0.75rem;
      border: 1px solid rgb(var(--c-gray-200));
    }
  }
  &.is-editable {
    .panel {
      position: relative;
      min-height: 3rem;
      cursor: pointer;
      &:hover {
        background: rgba(var(--c-black), 0.1);
      }
      .panel-icon {
        position: absolute;
        top: 0;
        right: 0;
        pointer-events: none;
      }
    }
  }
}
</style>
