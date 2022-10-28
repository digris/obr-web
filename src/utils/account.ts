import { watch } from "vue";
import { useIntervalFn } from "@vueuse/core";
import * as Sentry from "@sentry/vue";
import { isEqual } from "lodash-es";
import { useAccount } from "@/composables/account";
import eventBus from "@/eventBus";

const updateSentryScope = (user: any) => {
  Sentry.configureScope(function (scope) {
    scope.setUser(user);
  });
};

const updateOpenRelayScope = (user: any) => {
  const id = user ? user.email : null;
  if (window.tracker) {
    window.tracker.setUserID(id);
  }
};

class AccountHandler {
  constructor() {
    const { user, loadUser } = useAccount();
    watch(
      () => user.value,
      (newUser, oldUser) => {
        if (!isEqual(newUser, oldUser)) {
          updateSentryScope(newUser);
          updateOpenRelayScope(newUser);
        }
      }
    );
    const interval = 60 * 1000;
    useIntervalFn(async () => {
      await loadUser();
    }, interval);
  }
}

export default function () {
  return new AccountHandler();
}

// eslint-disable-next-line arrow-body-style
const requireSubscription = (fn: Function, message = "") => {
  // eslint-disable-next-line func-names
  return function (...args: any) {
    const { user, subscription } = useAccount();
    if (!user.value) {
      const event = {
        intent: "login",
        next: window.location.pathname,
        message,
      };
      eventBus.emit("account:authenticate", event);
      return false;
    }
    if (!subscription.value) {
      const event = {
        intent: "plan",
        next: window.location.pathname,
        message,
      };
      eventBus.emit("subscription:subscribe", event);
      return false;
    }
    if (subscription.value.isBlocked) {
      const event = {
        message: subscription.value.isBlocked,
      };
      eventBus.emit("geolocation:blocked", event);
      // alert(subscription.value.isBlocked);
      return false;
    }
    if (!subscription.value.isActive) {
      const event = {
        intent: "plan",
        next: window.location.pathname,
        message,
      };
      eventBus.emit("subscription:subscribe", event);
      return false;
    }
    // @ts-ignore
    return fn.apply(this, args);
  };
};

export { requireSubscription };
