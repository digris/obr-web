import { useRouter } from "vue-router";
import type { AxiosError } from "axios";

import { useAccount } from "@/composables/account";
import { useNotification } from "@/composables/notification";
import eventBus from "@/eventBus";

type TokenResult = {
  idToken?: {
    tokenString: string;
  };
};

type TokenPayload = {
  result: TokenResult;
};

export const useIdTokenLogin = () => {
  const { loginUserByGoogleIdToken, loadUser, user, isNew } = useAccount();
  const router = useRouter();
  const { notify } = useNotification();

  /*
    payload contains the whole data sent by obr-app
  */
  const loginByIdToken = async (payload: TokenPayload) => {
    const { result } = payload;

    const idToken = result?.idToken?.tokenString;
    if (!idToken) {
      return;
    }

    try {
      await loginUserByGoogleIdToken(idToken);
    } catch (err: unknown) {
      const error = err as AxiosError;
      const message = error.response?.data.message ?? "Login error";
      await notify({
        level: "error",
        body: `login error: ${message}`,
        ttl: 30,
      });
      return false;
    }

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
    return true;
  };
  return {
    loginByIdToken,
  };
};
