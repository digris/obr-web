import store from '@/store';
import eventBus from '@/eventBus';

class AccountHandler {
  constructor() {
    store.watch((state: any) => state.account.currentUser, async (newUser, oldUser) => {
      if (newUser !== oldUser) {
        await store.dispatch('rating/clearRatings');
      }
    });
  }
}

export default function () {
  return new AccountHandler();
}

// eslint-disable-next-line arrow-body-style
const requireLogin = (fn: Function, message: string) => {
  // eslint-disable-next-line func-names
  return function (...args: any) {
    const currentUser = store.getters['account/currentUser'];
    if (!currentUser) {
      const event = {
        intent: 'login',
        next: window.location.pathname,
        message,
      };
      eventBus.emit('account:authenticate', event);
      return false;
    }
    // @ts-ignore
    return fn.apply(this, args);
  };
};

// eslint-disable-next-line arrow-body-style
const requireSubscription = (fn: Function, message: string) => {
  // eslint-disable-next-line func-names
  return function (...args: any) {
    const currentUser = store.getters['account/currentUser'];
    if (!currentUser) {
      const event = {
        intent: 'login',
        next: window.location.pathname,
        message,
      };
      eventBus.emit('account:authenticate', event);
      return false;
    }
    if (!currentUser.subscription) {
      const event = {
        intent: 'trial',
        next: window.location.pathname,
        message,
      };
      eventBus.emit('subscription:subscribe', event);
      return false;
    }
    if (!currentUser.subscription.isActive) {
      const event = {
        intent: 'plan',
        next: window.location.pathname,
        message,
      };
      eventBus.emit('subscription:subscribe', event);
      return false;
    }
    // @ts-ignore
    return fn.apply(this, args);
  };
};

export { requireLogin, requireSubscription };
