import log from "loglevel";
import { useIntervalFn } from "@vueuse/core";
import { useDevice } from "@/composables/device";
import { usePlayerStore } from "@/stores/player";
import { useQueueStore } from "@/stores/queue";

const HEARTBEAT_INTERVAL = 1000;

// for channel options see:
// obr-app/obrapp/modules/OBRWebView.swift

// channels SENDING data TO swift-app
type sendChannel =
  | "heartbeat"
  | "global:init"
  // queue
  | "queue:deleteAtIndex"
  | "queue:playFromIndex"
  | "queue:enqueue"
  | "queue:enqueueAsNext"
  | "queue:enqueueToEnd"
  | "queue:shuffle"
  | "queue:clear"
  | "queue:requestUpdate" // initiates "queue:update"
  // player
  | "player:playLive"
  | "player:pause"
  | "player:resume"
  | "player:seek"
  | "player:requestUpdate" // initiates "player:update"
  // web
  | "web:setPath"
  // account
  | "account:setAccessToken"
  // browser
  | "browser:navigate";

// channels RECEIVING data FROM swift-app
type receiveChannel =
  // queue
  | "queue:update"
  // player
  | "player:update"
  // schedule
  | "schedule:update";

type SendMessage = {
  c: sendChannel;
  d?: string;
};

type ReceivedMessage = {
  c: receiveChannel;
  d?: string;
};

type ReceivedEventDetail = {
  c: receiveChannel;
  d?: string;
};

type ReceivedEvent = Event & {
  detail?: ReceivedEventDetail;
};

class AppBridge {
  constructor() {
    const { isWeb } = useDevice();
    if (isWeb) {
      log.debug("AppBridge - web mod detected: disable bridge");
      return;
    }
    log.debug("AppBridge - constructor");
    this.init().then(() => {
      log.debug("AppBridge - initialized");
    });
    useIntervalFn(
      async () => {
        await this.heartbeat();
      },
      HEARTBEAT_INTERVAL,
      { immediateCallback: true }
    );
    window.addEventListener("appBridge", this.onReceive.bind(this));
  }
  async init(): Promise<void> {
    log.debug("AppBridge - init");
    await this.send("global:init");
  }
  async heartbeat(): Promise<void> {
    // log.debug("AppBridge - heartbeat");
    await this.send("heartbeat");
  }
  // web > native - SEND payload TO swift-app channel
  async send(channel: sendChannel, data?: object) {
    if (channel !== "heartbeat") {
      log.debug("AppBridge - send", channel, data);
    }
    const message: SendMessage = {
      c: channel,
    };
    if (data) {
      message.d = JSON.stringify(data);
    }
    // @ts-ignore
    if (window.webkit) {
      // log.debug("payload", message);
      try {
        // @ts-ignore
        await window.webkit.messageHandlers.appBridge?.postMessage(message);
      } catch (e: unknown) {
        // console.warn(channel, e);
      }
    } else {
      log.debug("window.webkit not available");
    }
  }
  // web < native - handle RECEIVED data FROM swift-app channel
  async onReceive(e: ReceivedEvent) {
    if (!e.detail) {
      return;
    }
    const message: ReceivedMessage = e.detail;
    const channel = message.c;
    const data = message.d ? JSON.parse(message.d) : null;
    log.debug("AppBridge - onReceive", channel, data);

    switch (channel) {
      case "queue:update": {
        const { setQueueData } = useQueueStore();
        await setQueueData(data);
        break;
      }
      case "player:update": {
        const { setPlayerState } = usePlayerStore();
        const playerState = {
          ...data,
          // set missing dummy values
          bandwidth: 12800,
        };
        await setPlayerState(playerState);
        break;
      }
      case "schedule:update": {
        break;
      }
    }
  }
}

export { AppBridge };
