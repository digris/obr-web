// @ts-ignore
import scheduler from 'node-schedule';
import { refreshCredentials } from '@/api/account';

class CredentialsHandler {
  constructor() {
    const job = scheduler.scheduleJob('*/5 * * * * ', async () => {
      await refreshCredentials();
    });
    job.invoke();
  }
}

export default function () {
  return new CredentialsHandler();
}
