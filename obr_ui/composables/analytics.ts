import { type AnalyticsEvent, sendEvent, sendRawEvent } from "@/analytics/event";

const useAnalytics = () => {
  const logEvent = (kind: string, data?: object): void => {
    const evt = {
      kind,
      data,
    } as AnalyticsEvent;
    sendEvent(evt);
  };
  const logUIEvent = (action: string, value?: string | number | boolean | null): void => {
    logEvent("ui", {
      action,
      value,
    });
  };
  const logRawEvent = (kind: string, data?: object): void => {
    const evt = {
      kind,
      data,
    } as AnalyticsEvent;
    sendRawEvent(evt);
  };
  return {
    logEvent,
    logUIEvent,
    logRawEvent,
  };
};

export { useAnalytics };
