import { computed } from "vue";
import { useStore } from "vuex";

const useAccount = () => {
  const store = useStore();
  const user = computed(() => store.getters["account/user"]);
  return {
    user,
  };
};

export { useAccount };
