import { defineStore } from "pinia";

import {
  getUser,
  login,
  loginByGoogleIdToken,
  loginBySignedEmail,
  loginByToken,
  logout,
} from "@/api/account";

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
    async loginUser(credentials: Credentials) {
      const { email, password } = credentials;
      try {
        this.user = await login(email, password);
      } catch (err) {
        console.warn(err);
        this.user = null;
        throw err;
      }
    },
    async loginUserByToken(credentials: TokenCredentials) {
      const { email, token } = credentials;
      try {
        const { user, created } = await loginByToken(email, token);
        this.user = user;
        this.isNew = created;
        return {
          user,
          created,
        };
      } catch (err) {
        console.warn(err);
        this.user = null;
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
    async loginUserByGoogleIdToken(idToken: string) {
      try {
        const { user, created } = await loginByGoogleIdToken(idToken);
        this.user = user;
        this.isNew = created;
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
