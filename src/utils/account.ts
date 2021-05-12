import store from '@/store';

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
