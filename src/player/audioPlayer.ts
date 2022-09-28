// @ts-ignore
import shaka from "shaka-player";
// import shaka from "shaka-player/dist/shaka-player.compiled.debug";
import muxjs from "mux.js";
import notify from "@/utils/notification";
import { DateTime } from "luxon";
import { computed, ref, watch } from "vue";
import eventBus from "@/eventBus";
import store from "@/store";
import { usePlayerStore } from "@/stores/player";
import { playStream } from "@/player/stream";
import { useSettingsStore } from "@/stores/settings";
import { storeToRefs } from "pinia";
import { createAudioAnalyser } from "@/player/analyser";
import type { AudioAnalyser } from "@/player/analyser";

shaka.dependencies.add("muxjs", muxjs);

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

const POLL_INTERVAL = 100;

const PROTECTED_MEDIA = "https://media.next.openbroadcast.ch/";

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

class AudioPlayer {
  audio; // ref to html5 audio element

  player; // ref to shaka player

  playerState = {
    isLive: false,
    isStopped: true,
    isBuffering: false,
    isPaused: false,
    isPlaying: false,
    duration: null,
    currentTime: null,
  };

  startTime = 0;
  endTime = 0;
  fadeInTime = 0;
  fadeOutTime = 0;
  fadeVolume = ref(1);

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

    // TODO: does not need to run when player is idle..
    setInterval(() => {
      this.updateState();
    }, POLL_INTERVAL);

    eventBus.on("player:controls", (e) => {
      console.warn("DEPRECIATED: player:controls", e);
      switch (e.do) {
        case "play": {
          const { url, startTime } = e;
          this.play(url, startTime);
          break;
        }
        case "seek": {
          const { relPosition } = e;
          this.seek(relPosition);
          break;
        }
        case "stop": {
          this.stop();
          break;
        }
        case "pause": {
          this.pause();
          break;
        }
        case "resume": {
          this.resume();
          break;
        }
        default: {
          console.debug("unhandled action", e);
          break;
        }
      }
    });

    audio.onended = (e) => {
      console.debug("AudioPlayer - audio.onended", e);
      eventBus.emit("player:audio:ended", e);
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

  updateState() {
    const { updatePlayerState } = usePlayerStore();
    const { audio, player } = this;
    const stats = player.getStats();
    const isLive = player.isLive();
    const playheadTime = isLive ? player.getPlayheadTimeAsDate() : null;
    const bandwidth = Number.isNaN(stats.streamBandwidth) ? 0 : stats.streamBandwidth;
    let bufferState = null;
    let currentTime;
    let relPosition;
    if (stats.stateHistory.length) {
      // eslint-disable-next-line prefer-destructuring
      bufferState = stats.stateHistory.slice(-1)[0];
    }
    if (playheadTime) {
      currentTime = playheadTime;
      relPosition = null;
    } else {
      currentTime = audio.currentTime;
      relPosition = currentTime / audio.duration;
    }
    const playerState = {
      isLive,
      isStopped: true,
      isBuffering: !!(bufferState && bufferState.state === "buffering"),
      isPlaying: !!(bufferState && bufferState.state === "playing"),
      isPaused: audio.paused,
      // duration: audio.duration,
      duration: isLive ? null : audio.duration,
      bandwidth,
      currentTime,
      relPosition,
      playheadTime,
    };

    // if (Object.is(state, this.state)) {
    if (JSON.stringify(playerState) === JSON.stringify(this.playerState)) {
      return;
    }
    // @ts-ignore
    this.playerState = playerState;
    // TODO: refactor to pinia
    // store.dispatch("player/updatePlayerState", playerState);
    updatePlayerState(playerState);
    //
  }

  async onTimeupdate() {
    const ct = this.audio.currentTime;
    // cue-out
    if (this.endTime && ct > this.endTime) {
      console.debug("audioPlayer:onTimeupdate - end time reached");
      this.pause();
      await this.player.unload();
      await delay(1000);
      eventBus.emit("player:audio:ended");
    }
    // fade-in / out
    if (this.fadeInTime && this.startTime < ct && ct < this.fadeInTime) {
      const stepVolume = getFadeVolume(this.startTime, this.fadeInTime, ct);
      this.fadeVolume.value = stepVolume;
    } else if (this.fadeOutTime && this.endTime > ct && ct > this.fadeOutTime) {
      const stepVolume = getFadeVolume(this.fadeOutTime, this.endTime, ct, true);
      this.fadeVolume.value = stepVolume;
    } else if (ct) {
      if (this.fadeVolume.value !== 1) {
        this.fadeVolume.value = 1;
      }
    }
  }

  removeEventHandlers() {
    // console.debug("removeEventHandlers");
    this.audio.removeEventListener("timeupdate", this.onTimeupdate);
  }

  addEventHandlers() {
    this.removeEventHandlers();
    // console.debug("addEventHandlers", this);
    this.audio.addEventListener("timeupdate", this.onTimeupdate.bind(this), false);
  }

  async play(url: string, startTime = 0, endTime = 0, fadeIn = 0, fadeOut = 0) {
    console.debug("audioPlayer:play", {
      url,
      startTime,
      endTime,
      fadeIn,
      fadeOut,
    });
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
      console.error(e, url);
      notify({
        level: "error",
        ttl: 5,
        body: `Error ${e.code}: unable to play media.`,
      });
      console.debug("wait 2000ms");
      await delay(2000);
      console.debug("waited 2000ms");
      this.removeEventHandlers();
      return;
    }
    if (!this.analyser) {
      try {
        this.analyser = createAudioAnalyser(this.audio);
      } catch (e) {
        console.error(e);
      }
    }
    this.addEventHandlers();

    // this.player
    //   .load(url, startTime)
    //   .then(() => {
    //     this.audio.play();
    //   })
    //   .catch((e: Error) => {
    //     console.error(e);
    //     notify({
    //       level: "error",
    //       ttl: 5,
    //       body: `Error ${e.code}: unable to play media.`,
    //     });
    //   });
  }

  seek(relPosition: number) {
    if (!(this.playerState && this.playerState.duration)) {
      console.warn("unable to seek");
      return;
    }
    // @ts-ignore
    let absPosition = relPosition * this.playerState.duration;
    console.debug("seek", absPosition, this.endTime);
    if (this.startTime && absPosition < this.startTime) {
      this.fadeVolume.value = this.fadeInTime ? 0 : 1;
      absPosition = this.startTime;
    }
    if (this.endTime && absPosition > this.endTime) {
      return false;
    }
    this.audio.currentTime = absPosition;
    if (this.playerState.isPaused) {
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
      playStream();
      return;
    }
    this.audio.play();
  }
}

export { AudioPlayer };
