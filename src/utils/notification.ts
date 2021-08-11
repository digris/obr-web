import store from '@/store';
import { Message } from '@/store/notification';

const notify = async (message: Message) => {
  await store.dispatch('notification/addMessage', message);
};

export default notify;
