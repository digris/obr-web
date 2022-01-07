<script lang="ts">
import { computed, defineComponent } from 'vue';

export default defineComponent({
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
    //@include typo.large;
    padding-top: 0.75rem;
  }
  &.is-outlined {
    .panel {
      padding: 0.75rem;
      border: 1px solid rgb(var(--c-gray-200));
    }
  }
  &.is-editable {
    .panel {
      cursor: pointer;
      &:hover {
        background: rgba(var(--c-black), 0.1);
      }
    }
  }
}
</style>
