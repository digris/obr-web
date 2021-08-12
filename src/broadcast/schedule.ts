import scheduler from 'node-schedule';
import store from '@/store';

class Schedule {
  timeout: ReturnType<typeof setTimeout> | undefined;

  jobs: Array<any>;
  // jobs: Array<ReturnType<typeof scheduler.scheduleJob>>;

  constructor() {
    this.jobs = [];
    // add load interval & run immediately
    const rule = `${new Date().getSeconds()} * * * * *`;
    const maxJobAge = 61;
    // const rule = '*/10 * * * * *';
    const loadScheduleJob = scheduler.scheduleJob(rule, (scheduledDate: Date) => {
      if (scheduledDate && (+new Date() - +scheduledDate) > maxJobAge * 1000) {
        return;
      }
      Schedule.loadSchedule();
    });
    loadScheduleJob.invoke();

    // watch schedule updates
    /*
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
    */
    // store.watch((state: any, getters: any) => getters.time, (time) => {
    //   console.debug('time', time);
    // });
    // eslint-disable-next-line arrow-body-style
    store.watch((state: any, getters: any) => {
      return getters['time/time'];
    }, (time) => {
      const current = store.getters['schedule/current'];
      if (current && current.timeStart <= time && current.timeEnd > time) {
        // console.debug('current item matches - all fine!');
        return;
      }
      const schedule = store.getters['schedule/schedule'];
      if (!schedule.length) {
        // console.debug('schedule empty');
        return;
      }
      const newCurrent = schedule.find((s:any) => s.timeStart <= time && s.timeEnd > time);
      if (newCurrent) {
        Schedule.updateCurrent(newCurrent);
      }
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
