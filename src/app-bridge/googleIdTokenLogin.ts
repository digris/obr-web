import { useRouter } from "vue-router";

import { useAccount } from "@/composables/account";
import { useNotification } from "@/composables/notification";
import eventBus from "@/eventBus";

export const useIdTokenLogin = () => {
  const { loginUserByGoogleIdToken, loadUser, user, isNew } = useAccount();
  const router = useRouter();
  const { notify } = useNotification();

  /*
    payload contains the whole data sent by obr-app
  */
  const loginByIdToken = async (payload) => {
    const { result, status } = payload;
    console.debug("loginByIdToken", result, status);

    const idToken = result?.idToken?.tokenString;
    await loginUserByGoogleIdToken(idToken);
    await loadUser();

    eventBus.emit("side-menu:hide");

    if (isNew.value) {
      await router.push("/account/settings/");
    } else {
      await notify({
        level: "success",
        body: `logged in as ${user.value?.email}`,
        ttl: 3,
      });
    }
  };
  return {
    loginByIdToken,
  };
};
