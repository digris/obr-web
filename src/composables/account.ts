import { computed } from "vue";
import { storeToRefs } from "pinia";

import { useAccountStore } from "@/stores/account";

const useAccount = () => {
  const { user, subscription, address, settings } = storeToRefs(useAccountStore());
  const isStaff = computed(() => !!user.value?.isStaff);
  const isAdmin = computed(() => !!user.value?.isAdmin);
  // for unified handling we also pass along store actions here
  const { loginUser, logoutUser, loadUser, loginUserBySignedEmail, loginUserByToken } =
    useAccountStore();

  return {
    user,
    subscription,
    address,
    settings,
    isStaff,
    isAdmin,
    //
    loadUser,
    logoutUser,
    loginUser,
    loginUserBySignedEmail,
    loginUserByToken,
  };
};

export { useAccount };
