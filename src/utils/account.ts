import scheduler from 'node-schedule';
import store from '@/store';
import eventBus from '@/eventBus';

class AccountHandler {
  constructor() {
    store.watch((state: any) => state.account.user, async (newUser, oldUser) => {
      if (newUser !== oldUser) {
        await store.dispatch('rating/clearRatings');
      }
    });
    const rule = `${new Date().getSeconds()} * * * * *`;
    const maxJobAge = 61;
    scheduler.scheduleJob(rule, async (scheduledDate: Date) => {
      // @ts-ignore
      if (scheduledDate && (new Date() - scheduledDate) > maxJobAge * 1000) {
        return;
      }
      await store.dispatch('account/getUser');
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
    const user = store.getters['account/user'];
    if (!user) {
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
    const user = store.getters['account/user'];
    const subscription = store.getters['account/subscription'];
    if (!user) {
      const event = {
        intent: 'login',
        next: window.location.pathname,
        message,
      };
      eventBus.emit('account:authenticate', event);
      return false;
    }
    if (!subscription) {
      const event = {
        intent: 'plan',
        next: window.location.pathname,
        message,
      };
      eventBus.emit('subscription:subscribe', event);
      return false;
    }
    if (!subscription.isActive) {
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

export {
  requireLogin,
  requireSubscription,
};
