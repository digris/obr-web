import { defineStore } from "pinia";

import {
  getUser,
  login,
  loginByAppleId,
  loginByGoogleIdToken,
  loginBySignedEmail,
  loginByToken,
  logout,
} from "@/api/account";
import { useAnalytics } from "@/composables/analytics";

interface State {
  user: any | null;
  isNew: boolean;
}

export interface Credentials {
  email: string;
  password: string;
}

export interface TokenCredentials {
  email: string;
  token: string;
}

export const useAccountStore = defineStore("account", {
  state: (): State => ({
    user: null,
    isNew: false,
  }),
  persist: true,
  getters: {
    subscription: (state: State) => {
      return state.user?.subscription;
    },
    address: (state: State) => {
      return state.user?.address;
    },
    settings: (state: State) => {
      return state.user?.settings;
    },
  },
  actions: {
    // reusable references to analytics (will be changed when refactoring store to composition API)
    logUserEvent(action: string, value?: string | number | boolean | null) {
      const { logEvent } = useAnalytics();
      logEvent("user", { action, value });
    },
    async loginUser(credentials: Credentials) {
      const { email, password } = credentials;
      try {
        this.user = await login(email, password);
        this.logUserEvent("login", "local");
      } catch (err: any) {
        console.warn(err);
        this.user = null;
        this.logUserEvent("login-failed", err?.response?.statusText);
        throw err;
      }
    },
    async loginUserByToken(credentials: TokenCredentials) {
      const { email, token } = credentials;
      try {
        const { user, created } = await loginByToken(email, token);
        this.user = user;
        this.isNew = created;
        if (created) {
          this.logUserEvent("signup", "token");
        }
        this.logUserEvent("login", "token");
        return {
          user,
          created,
        };
      } catch (err: any) {
        console.warn(err);
        this.user = null;
        this.logUserEvent("login-failed", err?.response?.statusText);
        throw err;
      }
    },
    async loginUserBySignedEmail(signedEmail: string) {
      try {
        this.user = await loginBySignedEmail(signedEmail);
      } catch (err) {
        console.warn(err);
        this.user = null;
        throw err;
      }
    },
    async loginUserByAppleId(idToken: string, authorizationCode: string, profile: object) {
      console.debug("loginUserByAppleId", idToken, authorizationCode, profile);
      try {
        const { user, created } = await loginByAppleId(idToken, authorizationCode, profile);
        this.user = user;
        this.isNew = created;
        if (created) {
          this.logUserEvent("signup", "apple");
        }
        this.logUserEvent("login", "apple");
      } catch (err) {
        console.warn(err);
        this.user = null;
        throw err;
      }
    },
    async loginUserByGoogleIdToken(idToken: string) {
      console.debug("loginUserByGoogleIdToken", idToken);
      try {
        const { user, created } = await loginByGoogleIdToken(idToken);
        this.user = user;
        this.isNew = created;
        if (created) {
          this.logUserEvent("signup", "google");
        }
        this.logUserEvent("login", "google");
      } catch (err) {
        console.warn(err);
        this.user = null;
        throw err;
      }
    },
    async logoutUser() {
      try {
        await logout();
        this.user = null;
        this.logUserEvent("logout");
      } catch (err) {
        console.warn(err);
        throw err;
      }
    },
    async loadUser() {
      try {
        this.user = await getUser();
      } catch (err) {
        console.warn(err);
        throw err;
      }
    },
  },
});
