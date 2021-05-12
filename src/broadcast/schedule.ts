// @ts-ignore
import { DateTime } from 'luxon';
// @ts-ignore
import scheduler from 'node-schedule';
import store from '@/store';

const JOB_MAX_AGE = 60;

class Schedule {
  timeout: ReturnType<typeof setTimeout> | undefined;

  jobs: Array<any>;
  // jobs: Array<ReturnType<typeof scheduler.scheduleJob>>;

  constructor() {
    this.jobs = [];
    // add load interval & run immediately
    const rule = `${new Date().getSeconds()} * * * * *`;
    // const rule = '*/10 * * * * *';
    const loadScheduleJob = scheduler.scheduleJob(rule, (scheduledDate: Date) => {
      // @ts-ignore
      if (scheduledDate && (new Date() - scheduledDate) > JOB_MAX_AGE * 1000) {
        return;
      }
      Schedule.loadSchedule();
    });
    loadScheduleJob.invoke();

    // watch schedule updates
    store.watch((state: any) => state.schedule.schedule, (schedule) => {
      // cancel all pending jobs & reset array
      this.jobs.forEach((job) => {
        job.cancel();
      });
      this.jobs = [];

      // loop whole loaded schedule, create / update job upcoming entries
      const now = DateTime.now();
      const until = DateTime.now().plus({ minutes: 15 });

      const current = schedule.find((s:any) => s.timeStart <= now && s.timeEnd > now);
      if (current) {
        Schedule.updateCurrent(current);
      }

      const upcoming = schedule.filter((s:any) => s.timeStart >= now && s.timeStart < until);
      upcoming.forEach((item:any) => {
        // times are luxon `DateTime` instances. using `ts` for native date compatibility
        const runAt = item.timeStart.ts;
        // eslint-disable-next-line prefer-arrow-callback, func-names
        const job = scheduler.scheduleJob(runAt, function () {
          // store.dispatch('schedule/updateCurrent', item);
          Schedule.updateCurrent(item);
        }.bind(null, item));
        this.jobs.push(job);
      });
    });
  }

  static async loadSchedule() {
    await store.dispatch('schedule/loadSchedule');
  }

  static async updateCurrent(item: any) {
    const current = store.getters['schedule/current'];
    if (current && current.key === item.key) {
      return;
    }
    await store.dispatch('schedule/updateCurrent', item);
  }
}

export default function () {
  return new Schedule();
}
