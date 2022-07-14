import { useIntervalFn } from "@vueuse/core";
import * as Sentry from "@sentry/vue";
import { isEqual } from "lodash-es";
import store from "@/store";
import eventBus from "@/eventBus";

const updateSentryScope = (user: any) => {
  Sentry.configureScope(function (scope) {
    scope.setUser(user);
  });
};

const updateOpenRelayScope = (user: any) => {
  const id = user ? user.email : null;
  // @ts-ignore
  window.tracker.setUserID(id);
};

class AccountHandler {
  constructor() {
    store.watch(
      (state: any) => state.account.user,
      async (newUser, oldUser) => {
        if (!isEqual(newUser, oldUser)) {
          updateSentryScope(newUser);
          updateOpenRelayScope(newUser);
          // await store.dispatch('rating/clearRatings');
        }
      }
    );
    const interval = 60 * 1000;
    useIntervalFn(async () => {
      await store.dispatch("account/getUser");
    }, interval);
    // const focused = useWindowFocus();
    // watch(focused, (value) => {
    //   console.debug('focused', value);
    // });
  }
}

export default function () {
  return new AccountHandler();
}

// eslint-disable-next-line arrow-body-style
const requireSubscription = (fn: Function, message = "") => {
  // eslint-disable-next-line func-names
  return function (...args: any) {
    const user = store.getters["account/user"];
    const subscription = store.getters["account/subscription"];
    if (!user) {
      const event = {
        intent: "login",
        next: window.location.pathname,
        message,
      };
      eventBus.emit("account:authenticate", event);
      return false;
    }
    if (!subscription) {
      const event = {
        intent: "plan",
        next: window.location.pathname,
        message,
      };
      eventBus.emit("subscription:subscribe", event);
      return false;
    }
    if (!subscription.isActive) {
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
