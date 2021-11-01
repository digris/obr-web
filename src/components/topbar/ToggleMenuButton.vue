<script type="ts">
import { computed, defineComponent } from 'vue';
import { useStore } from 'vuex';
import CircleButton from '@/components/ui/button/CircleButton.vue';
import IconMenu from '@/components/ui/icon/IconMenu.vue';

export default defineComponent({
  components: {
    CircleButton,
    IconMenu,
  },
  setup() {
    const store = useStore();
    const user = computed(() => store.getters['account/user']);
    const initials = computed(() => {
      if (!user.value) {
        return '?';
      }
      if (user.value.firstName) {
        return user.value.firstName.substr(0, 1).toUpperCase();
      }
      return user.value.email.substr(0, 1).toUpperCase();
    });
    return {
      user,
      initials,
    };
  },
});
</script>

<template>
  <CircleButton
    :size="(48)"
    :outlined="(false)"
    :active="(true)"
    v-if="user"
    v-text="initials"
  />
  <CircleButton
    :size="(48)"
    :outlined="(false)"
    v-else
  >
    <IconMenu
      :size="(48)"
    />
  </CircleButton>
</template>
