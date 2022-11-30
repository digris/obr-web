import log from "loglevel";
// @ts-ignore
import shaka from "shaka-player";
// import shaka from "shaka-player/dist/shaka-player.compiled.debug";
// @ts-ignore
import muxjs from "mux.js";
import { computed, ref, watch } from "vue";
import { isEqual, round } from "lodash-es";
import type { AudioAnalyser } from "@/player/analyser";
import type { PlayerState } from "@/stores/player";
import { useDevice } from "@/composables/device";
import { usePlayerStore } from "@/stores/player";
import { usePlayerControls } from "@/composables/player";
import { useSettingsStore } from "@/stores/settings";
import { useQueueControls } from "@/composables/queue";
import { storeToRefs } from "pinia";
import { createAudioAnalyser } from "@/player/analyser";

shaka.dependencies.add("muxjs", muxjs);

const POLL_INTERVAL = 100;

const PROTECTED_MEDIA = "https://media.next.openbroadcast.ch/";

const SHAKA_CONFIG = {
  manifest: {
    dash: {
      ignoreMinBufferTime: true,
    },
  },
  abr: {
    switchInterval: 2,
    defaultBandwidthEstimate: 1000000, // 10 Mbit/s
    bandwidthDowngradeTarget: 0.4,
    bandwidthUpgradeTarget: 0.2,
    // NOTE: testing bw limitations
    // restrictions: {
    //   maxBandwidth: 512000,
    // },
  },
  streaming: {
    bufferingGoal: 30,
    rebufferingGoal: 0.1,
    bufferBehind: 0.1,
    retryParameters: {
      maxAttempts: 100,
    },
    useNativeHlsOnSafari: false,
  },
};

// eslint-disable-next-line no-unused-vars
// @ts-ignore
const requestFilter = (type, request) => {
  // we need a dynamic way to switch on / off
  // `allowCrossSiteCredentials` (signed cookies for on-demand content via GCP / CDN)
  if (request.uris.findIndex((uri: string) => uri.startsWith(PROTECTED_MEDIA)) === 0) {
    /* eslint-disable-next-line no-param-reassign */
    request.allowCrossSiteCredentials = true;
  }
};

const getFadeVolume = (start: number, end: number, time: number, reverse = false) => {
  const duration = end - start;
  const position = time - start;
  const vol = position / duration;
  const vol2 = reverse ? 1 - vol : vol;
  return Math.sin((vol2 * Math.PI) / 2);
  // return vol ? Math.log(vol * 100) / Math.log(100) : 0;
};

const delay = (ms: number) => new Promise((res) => setTimeout(res, ms));

// get current shaka player buffer state
// either "playing" or "buffering"
const getBufferState = (stats: any): "playing" | "buffering" | null => {
  const lastState = stats?.stateHistory?.length ? stats.stateHistory.slice(-1)[0] : null;
  if (lastState) {
    return lastState.state;
  }
  return null;
};

// get current audio element state
// either "playing" or "buffering"
const getAudioState = (audio: HTMLAudioElement): "paused" | "stopped" => {
  if (audio.paused) {
    return "paused";
  }
  return "stopped";
};

class AudioPlayer {
  audio; // ref to html5 audio element

  player; // ref to shaka player

  playerState: PlayerState = {
    mode: "live",
    state: "stopped",
    duration: null,
    absPosition: null,
    bandwidth: 0,
  };

  isUnblocked = false;

  startTime = 0;
  endTime = 0;
  fadeInTime = 0;
  fadeOutTime = 0;
  fadeVolume = ref(1);

  // actions from pinia store need to be mapped in the constructor
  // as the store is not ready earlier
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  setPlayerState = async (s: PlayerState): Promise<void> => {};
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  setLiveLatency = async (l: number): Promise<void> => {};

  analyser: AudioAnalyser | null;

  constructor() {
    // `audio` is the html5 audio element
    // `player` is the shaka player instance
    const audio = document.createElement("audio");
    const player = new shaka.Player(audio);
    const networkingEngine = player.getNetworkingEngine();
    // set initial configuration & register network filters
    player.configure(SHAKA_CONFIG);
    networkingEngine.registerRequestFilter(requestFilter);

    this.analyser = null;

    this.audio = audio;
    this.player = player;
    // add to window for debug access
    // @ts-ignore
    window.audio = audio;
    // @ts-ignore
    window.player = player;

    // map store actions to class
    const { setPlayerState: setPlayerStateFn, setLiveLatency: setLiveLatencyFn } = usePlayerStore();
    this.setPlayerState = setPlayerStateFn;
    this.setLiveLatency = setLiveLatencyFn;

    // TODO: does not need to run when player is idle..
    setInterval(async () => {
      await this.updateState();
    }, POLL_INTERVAL);

    const { playNext } = useQueueControls();
    audio.onended = async (e) => {
      log.debug("AudioPlayer - audio.onended", e);
      // eventBus.emit("player:audio:ended", e);
      await playNext();
    };

    const { volume, maxBandwidth } = storeToRefs(useSettingsStore());

    if (maxBandwidth.value > 0) {
      this.updateMaxBandwidth(maxBandwidth.value);
    }

    const playbackVolume = computed(() => {
      return volume.value * this.fadeVolume.value;
    });

    if (volume.value > -1) {
      this.updateVolume(playbackVolume.value);
    }

    watch(
      () => playbackVolume.value,
      (newValue) => {
        this.updateVolume(newValue);
      }
    );

    watch(
      () => maxBandwidth.value,
      (newValue) => {
        this.updateMaxBandwidth(newValue);
      }
    );
  }
  updateVolume(value: number) {
    this.audio.volume = value / 100.0;
  }
  updateMaxBandwidth(value: number) {
    this.updateSettings({
      abr: {
        restrictions: {
          maxBandwidth: value > 0 ? value : null,
        },
      },
    });
  }
  updateSettings(settings: any) {
    this.player.configure(settings);
  }
  // runs as interval
  // collect player information and send them to the store
  async updateState(): Promise<void> {
    const { audio, player } = this;
    // get current values from shaka player
    const stats = player.getStats();
    const isLive = player.isLive();
    const mode = isLive ? "live" : "ondemand";

    const bufferState = getBufferState(stats);
    const audioState = getAudioState(audio);
    // use shaka player buffer state or fallback to audio element's value
    const state = bufferState ? bufferState : audioState;
    //
    const duration = isLive ? null : audio.duration;
    const absPosition = isLive ? null : audio.currentTime;
    const bandwidth = Number.isNaN(stats.streamBandwidth) ? 0 : stats.streamBandwidth;

    const playerState: PlayerState = {
      mode,
      state,
      duration: Number.isNaN(duration) ? 0 : duration,
      absPosition,
      bandwidth,
    };

    if (!Number.isNaN(stats.liveLatency)) {
      await this.setLiveLatency(round(stats.liveLatency, 2));
    }

    // stop here if no change in the state
    if (isEqual(playerState, this.playerState)) {
      return;
    }

    // log.debug(playerState);
    this.playerState = playerState;
    await this.setPlayerState(playerState);
  }

  async onTimeupdate() {
    const { isIos } = useDevice();
    const ct = this.audio.currentTime;
    // cue-out
    if (this.endTime && ct > this.endTime) {
      log.debug("audioPlayer:onTimeupdate - end time reached");
      if (isIos) {
        log.debug("device is iOS - we ignore queue outs for the moment as it does not work...");
        return;
      }
      this.pause();
      await this.player.unload();
      await delay(5);
      const { playNext } = useQueueControls();
      await playNext();
      // eventBus.emit("player:audio:ended");
    }
    // fade-in / out
    if (this.fadeInTime && this.startTime < ct && ct < this.fadeInTime) {
      const stepVolume = getFadeVolume(this.startTime, this.fadeInTime, ct);
      this.fadeVolume.value = stepVolume;
    } else if (this.fadeOutTime && this.endTime > ct && ct > this.fadeOutTime) {
      if (isIos) {
        // we ignore fade outs for the moment, see above
        return;
      }
      const stepVolume = getFadeVolume(this.fadeOutTime, this.endTime, ct, true);
      this.fadeVolume.value = stepVolume;
    } else if (ct) {
      if (this.fadeVolume.value !== 1) {
        this.fadeVolume.value = 1;
      }
    }
  }

  removeEventHandlers() {
    // log.debug("removeEventHandlers");
    this.audio.removeEventListener("timeupdate", this.onTimeupdate);
  }

  addEventHandlers() {
    this.removeEventHandlers();
    // log.debug("addEventHandlers", this);
    this.audio.addEventListener("timeupdate", this.onTimeupdate.bind(this), false);
  }

  // un-block safari playback.
  // this has to be invoked by a user-interaction (click / tap)
  async unblockPlay() {
    log.debug("AudioPlayer - unblock");
    if (this.isUnblocked) {
      log.debug("AudioPlayer - already unblocked - nothing to do");
      return;
    }
    log.debug("AudioPlayer - load & play silence");
    // set source to base64 encode 0.001s audio
    this.audio.src =
      "data:audio/wav;base64,UklGRsgAAABXQVZFZm10ICgAAAD+/wIAgD4AAAD0AQAIACAAFgAgAAMAAAABAAAAAAAQAIAAAKoAOJtxZmFjdAQAAAAQAAAAZGF0YYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==";
    await audio.play();
    this.isUnblocked = true;
    log.debug("AudioPlayer - un-blocked");
  }

  async play(url: string, startTime = 0, endTime = 0, fadeIn = 0, fadeOut = 0) {
    log.debug("audioPlayer:play", {
      url,
      startTime,
      endTime,
      fadeIn,
      fadeOut,
    });

    await this.unblockPlay();

    // load url to shaka player, then trigger 'play' on audio element
    this.startTime = startTime;
    this.endTime = endTime;
    this.fadeInTime = fadeIn ? startTime + fadeIn : 0;
    this.fadeOutTime = fadeOut ? endTime - fadeOut : 0;
    this.fadeVolume.value = fadeIn ? 0 : 1;
    if (fadeIn) {
      this.audio.volume = 0;
    }

    try {
      await this.player.load(url, startTime);
      this.audio.play();
    } catch (e) {
      log.error(e, url);
      await delay(50);
      this.removeEventHandlers();
      throw Error("playback error");
    }
    if (!this.analyser) {
      try {
        this.analyser = createAudioAnalyser(this.audio);
      } catch (e) {
        log.error(e);
      }
    }
    this.addEventHandlers();
  }

  seek(relPosition: number) {
    if (!(this.playerState && this.playerState.duration)) {
      log.warn("unable to seek");
      return;
    }
    // @ts-ignore
    let absPosition = relPosition * this.playerState.duration;
    log.debug("seek", absPosition);
    if (this.startTime && absPosition < this.startTime) {
      this.fadeVolume.value = this.fadeInTime ? 0 : 1;
      absPosition = this.startTime;
    }
    if (this.endTime && absPosition > this.endTime) {
      return false;
    }
    this.audio.currentTime = absPosition;
    if (this.playerState.state === "paused") {
      this.resume();
    }
  }

  stop() {
    this.player.unload();
  }

  pause() {
    this.audio.pause();
  }

  resume() {
    if (this.player.isLive()) {
      const { playLive } = usePlayerControls();
      playLive();
      return;
    }
    this.audio.play();
  }
}

export { AudioPlayer };
