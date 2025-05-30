import { watch } from "vue";
import * as Sentry from "@sentry/vue";
import { useIntervalFn } from "@vueuse/core";
import { isEqual } from "lodash-es";

import { useAccount } from "@/composables/account";
import { useAnalytics } from "@/composables/analytics";
import { useDevice } from "@/composables/device";
import { useSubscription } from "@/composables/subscription";
import eventBus from "@/eventBus";
import type { User } from "@/typings/api";

const FAST_POLLING_INTERVAL = 60 * 1000;
const SLOW_POLLING_INTERVAL = 5 * 60 * 1000;

const updateAppBridgeAccount = (user: User) => {
  if (window.appBridge) {
    const channel = "account:setAccessToken";
    const data = {
      accessToken: user?.accessToken ?? null,
    };
    window.appBridge.send(channel, data);
  }
};

const updateSentryScope = (user: User) => {
  Sentry.configureScope(function (scope) {
    scope.setUser(user);
  });
};

class AccountHandler {
  constructor() {
    const { user, loadUser } = useAccount();
    const { loadUserVouchers } = useSubscription();
    const { isApp } = useDevice();
    watch(
      () => user.value,
      (newUser, oldUser) => {
        if (!isEqual(newUser?.uid, oldUser?.uid)) {
          if (isApp) {
            updateAppBridgeAccount(newUser);
          }
          updateSentryScope(newUser);
        }
      }
    );
    useIntervalFn(async () => {
      await loadUser();
    }, FAST_POLLING_INTERVAL);
    useIntervalFn(
      async () => {
        await loadUserVouchers();
      },
      SLOW_POLLING_INTERVAL,
      { immediateCallback: true }
    );
  }
}

export default function () {
  return new AccountHandler();
}

// eslint-disable-next-line arrow-body-style, @typescript-eslint/ban-types
const requireSubscription = (fn: Function, message = "") => {
  // eslint-disable-next-line func-names
  return function (...args: any) {
    const { user, subscription } = useAccount();
    const { logUIEvent } = useAnalytics();
    if (!user.value) {
      const event = {
        intent: "login",
        next: window.location.pathname,
        message,
      };
      eventBus.emit("account:authenticate", event);
      logUIEvent("subscription:paywall", "unauthenticated");
      return false;
    }
    if (!subscription.value) {
      const event = {
        intent: "voucher",
        next: window.location.pathname,
        message,
      };
      eventBus.emit("subscription:subscribe", event);
      logUIEvent("subscription:paywall", "no-subscription");
      return false;
    }
    if (subscription.value.isBlocked) {
      const event = {
        message: subscription.value.isBlocked,
      };
      eventBus.emit("geolocation:blocked", event);
      logUIEvent("subscription:paywall", "geo-blocked");
      return false;
    }
    if (!subscription.value.isActive) {
      const event = {
        intent: "voucher",
        next: window.location.pathname,
        message,
      };
      eventBus.emit("subscription:subscribe", event);
      logUIEvent("subscription:paywall", "inactive-subscription");
      return false;
    }
    // @ts-ignore
    return fn.apply(this, args);
  };
};

export { requireSubscription };
