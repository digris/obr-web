import { storeToRefs } from "pinia";

import { useSubscriptionStore } from "@/stores/subscription";

export const useSubscription = () => {
  const { userVouchers } = storeToRefs(useSubscriptionStore());
  const { loadUserVouchers } = useSubscriptionStore();

  return {
    userVouchers,
    loadUserVouchers,
  };
};
