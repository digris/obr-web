import { useIntervalFn } from "@vueuse/core";
import log from "loglevel";

import { useAccount } from "@/composables/account";
import { useDevice } from "@/composables/device";
import { usePlayerStore } from "@/stores/player";
import { useQueueStore } from "@/stores/queue";
import { useScheduleStore } from "@/stores/schedule";
import { useSettingsStore } from "@/stores/settings";

import { useAppleIdLogin } from "./appleIdLogin";
import { useGoogleIdTokenLogin } from "./googleIdTokenLogin";

// how often the web-app sends a heartbeat to swift-app
const HEARTBEAT_INTERVAL = 2000 * 0.9;

// configuration for swift-app
const HEARTBEAT_APP_ACTIVE_DELAY = 2.0;
const HEARTBEAT_APP_FOREGROUND_DELAY = 2.0;
const HEARTBEAT_HEARTBEAT_DELAY = 2.0;

// for channel options see:
// obr-app/obrapp/modules/OBRWebView.swift

// channels SENDING data TO swift-app
type sendChannel =
  | "heartbeat"
  | "heartbeat:setDelays"
  | "heartbeat:shutdown"
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
  // ui
  | "ui:setTheme"
  // rating
  | "rating:setRatings"
  // settings
  | "settings:setMaxBandwidth"
  // account
  | "account:setAccessToken"
  // browser
  | "browser:navigate"
  // sign-in
  | "googleSignin:start"
  | "appleSignin:start";

// channels RECEIVING data FROM swift-app
type receiveChannel =
  // queue
  | "queue:update"
  // player
  | "player:update"
  // schedule
  | "schedule:update"
  // ui
  | "ui:update"
  // rating
  | "rating:update"
  // settings
  | "settings:update"
  // settings
  | "account:update"
  // appscene
  | "appscene:update"
  // sign-in
  | "googleSignin:completed"
  | "appleSignin:completed";

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
  static instance: AppBridge;

  pauseHeartbeat = (): void => {};

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  loginByAppleId = async (payload: unknown): Promise<void> => {};

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  loginByGoogleIdToken = async (payload: unknown): Promise<void> => {};

  private constructor() {
    const { isApp } = useDevice();

    if (!isApp) {
      log.info("AppBridge only available in app-mode");
      return;
    }

    log.debug("AppBridge - constructor");
    this.init().then(() => {
      log.debug("AppBridge - initialized");
    });
    const { pause: pauseHeartbeat } = useIntervalFn(
      async () => {
        await this.heartbeat();
      },
      HEARTBEAT_INTERVAL,
      { immediateCallback: true }
    );
    this.pauseHeartbeat = async () => {
      log.debug("AppBridge - pauseHeartbeat");
      pauseHeartbeat();
      await this.send("heartbeat:shutdown");
    };
    window.addEventListener("appBridge", this.onReceive.bind(this));

    // in app-mode we have to handle link-clicks separately
    // NOTE: mailto: etc. links should be implemented in swift / webview. example:
    // https://gist.github.com/dakeshi/d8e69e4ba50b31211d94
    window.addEventListener("click", this.onExternalLink.bind(this));

    // we need to initiate use*IdTokenLogin here to have access to router etc.
    const { loginByAppleId } = useAppleIdLogin();
    this.loginByAppleId = loginByAppleId;

    const { loginByGoogleIdToken } = useGoogleIdTokenLogin();
    this.loginByGoogleIdToken = loginByGoogleIdToken;
  }

  public static getInstance(): AppBridge {
    if (!AppBridge.instance) {
      AppBridge.instance = new AppBridge();
    }
    return AppBridge.instance;
  }

  async init(): Promise<void> {
    log.debug("AppBridge - init");
    await this.send("global:init");
    const delays = {
      appActiveDelay: HEARTBEAT_APP_ACTIVE_DELAY,
      appForegroundDelay: HEARTBEAT_APP_FOREGROUND_DELAY,
      heartbeatDelay: HEARTBEAT_HEARTBEAT_DELAY,
    };
    await this.send("heartbeat:setDelays", delays);

    // send accessToken in case of existing user session
    const { user } = useAccount();
    if (user.value?.accessToken) {
      await this.send("account:setAccessToken", { accessToken: user.value?.accessToken });
    }
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
          playState: data.state, // NOTE: should be adjusted in obr-app
          currentTime: data.absPosition, // NOTE: should be adjusted in obr-app
          ...data,
          // set missing dummy values
          bandwidth: 12800,
        };
        await setPlayerState(playerState);
        break;
      }
      case "settings:update": {
        const { setMaxBandwidth, setShuffleMode } = useSettingsStore();
        setMaxBandwidth(data.maxBandwidth);
        setShuffleMode(data.shuffleMode);
        break;
      }
      case "schedule:update": {
        console.debug("schedule", data.schedule);
        const { setSchedule } = useScheduleStore();
        await setSchedule(data.schedule);
        break;
      }
      case "account:update": {
        break;
      }
      case "appscene:update": {
        // for some reason the app "looses" the accessToken / cdnKey
        // so we force an update here...
        const { sceneName, eventName } = data;
        if (sceneName === "Main" && eventName === "sceneDidBecomeActive") {
          console.debug("appscene", "mainSceneDidBecomeActive");
          const { user } = useAccount();
          if (user.value?.accessToken) {
            await this.send("account:setAccessToken", { accessToken: user.value?.accessToken });
          }
        }
        break;
      }
      case "appleSignin:completed": {
        console.debug("appleSignin:completed", data);
        await this.loginByAppleId(data);
        break;
      }
      case "googleSignin:completed": {
        // console.debug("googleSignin:completed", data);
        await this.loginByGoogleIdToken(data);
        break;
      }
    }
  }
  async onExternalLink(e: Event) {
    const origin = (e.target as Element).closest("a");
    if (!origin) {
      return;
    }
    // links with `target="_blank"` should open in native safari
    if (origin.target === "_blank") {
      e.preventDefault();
      await this.send("browser:navigate", {
        url: origin.href,
      });
      return;
    }
    // "mailto" links should open in native safari
    if (origin.href.startsWith("mailto:")) {
      e.preventDefault();
      await this.send("browser:navigate", {
        url: origin.href,
      });
      return;
    }
    // stop evaluation for "internal" links
    if (origin.host && origin.host === window.location.host) {
      return;
    }
    // "external" links should open in native safari
    // (assuming we dont have any http:// links...)
    if (origin.href.startsWith("https://")) {
      e.preventDefault();
      await this.send("browser:navigate", {
        url: origin.href,
      });
      return;
    }
  }
}

export { AppBridge };
