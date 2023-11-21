<script lang="ts">
import { computed, defineComponent } from "vue";

import { useAccount } from "@/composables/account";
import { useObjKey } from "@/composables/obj";

import Identifier from "./Identifier.vue";

export default defineComponent({
  components: {
    Identifier,
  },
  props: {
    obj: {
      type: Object,
      required: true,
    },
    limit: {
      type: Number,
      default: 8,
    },
    separator: {
      type: String,
      default: ", ",
    },
    spacing: {
      type: String,
      default: "0.5rem",
    },
  },
  setup(props) {
    const { isStaff } = useAccount();
    const { objKey } = useObjKey(props.obj);
    const keyPrefix = computed(() => props.obj?.uid);
    const objIdentifiers = computed(() => {
      // eslint-disable-next-line max-len
      return props.obj && props.obj.identifiers
        ? props.obj.identifiers.slice(0, props.limit - 1)
        : [];
    });
    const extraIdentifiers = computed(() => {
      if (isStaff.value) {
        return [
          {
            scope: "obp",
            value: `/api/v1/redirect/obp/${objKey.value}/`,
          },
        ];
      }
      return [];
    });
    const identifiers = computed(() => {
      return [...objIdentifiers.value, ...extraIdentifiers.value];
    });
    return {
      objKey,
      keyPrefix,
      identifiers,
      isStaff,
    };
  },
});
</script>

<template>
  <div
    class="identifiers"
    :style="{
      '--spacing': spacing,
    }"
  >
    <Identifier
      class="identifiers__identifier"
      v-for="identifier in identifiers"
      :key="`obj-identifier-${keyPrefix}-${identifier?.uid ?? ''}`"
      :scope="identifier.scope"
      :value="identifier.value"
    />
  </div>
</template>

<style lang="scss" scoped>
.identifiers {
  &__identifier {
    &:not(:last-child) {
      margin-right: var(--spacing);
    }
  }
}
</style>
