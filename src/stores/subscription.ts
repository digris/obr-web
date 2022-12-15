import { defineStore } from "pinia";

import { getUserVouchers } from "@/api/subscription";
import type { UserVoucher } from "@/typings/api";

interface State {
  userVouchers: Array<UserVoucher>;
}

export const useSubscriptionStore = defineStore("subscription", {
  state: (): State => ({
    userVouchers: [],
  }),
  actions: {
    async loadUserVouchers() {
      try {
        this.userVouchers = await getUserVouchers();
      } catch (err) {
        console.warn(err);
        throw err;
      }
    },
  },
});
