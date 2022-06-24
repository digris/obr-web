import { computed } from "vue";
import { useStore } from "vuex";

const useAccount = () => {
  const store = useStore();
  const user = computed(() => store.getters["account/user"]);
  const isStaff = computed(() => {
    return !!user.value?.isStaff;
  });
  const isAdmin = computed(() => {
    return !!user.value?.isAdmin;
  });
  return {
    user,
    isStaff,
    isAdmin,
  };
};

export { useAccount };
