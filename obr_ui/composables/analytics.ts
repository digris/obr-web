import { type AnalyticsEvent, sendEvent } from "@/analytics/event";

const useAnalytics = () => {
  const logUIAction = (action: string, value?: string | number | boolean | null): void => {
    const evt = {
      kind: "ui",
      data: {
        action,
        value,
      },
    } as AnalyticsEvent;
    sendEvent(evt);
  };

  return {
    logUIAction,
  };
};

export { useAnalytics };
