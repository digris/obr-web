// @ts-ignore
import scheduler from 'node-schedule';
import { refreshCredentials } from '@/api/account';

const JOB_MAX_AGE = 300;

class CredentialsHandler {
  constructor() {
    const job = scheduler.scheduleJob('*/5 * * * * ', async (scheduledDate: Date) => {
      // @ts-ignore
      if (scheduledDate && (new Date() - scheduledDate) > JOB_MAX_AGE * 1000) {
        return;
      }
      await refreshCredentials();
    });
    job.invoke();
  }
}

export default function () {
  return new CredentialsHandler();
}
