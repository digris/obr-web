import mitt from "mitt";

export type EventBusEvents = {
  //
  "account:authenticate": {
    intent: string;
    next: string;
  };
  //
  "subscription:subscribe": {
    intent: string;
    next?: string;
    message?: string;
  };
  //
  "geolocation:blocked": {
    message: string;
  };
  //
  "radio:flow": "reset" | "releaseFocus" | "focusNext" | "focusPrevious";
  //
  "side-menu:show": void;
  "side-menu:hide": void;
  "global-search:show": void;
};

const eventBus = mitt<EventBusEvents>();

// eventBus.on("*", (type, e) => console.log(type, e));

window.eventBus = eventBus;

export default eventBus;
