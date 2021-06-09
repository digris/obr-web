// @ts-ignore
import shaka from 'shaka-player';
import { DateTime } from 'luxon';
import eventBus from '@/eventBus';
import store from '@/store';

const SHAKA_CONFIG = {
  manifest: {
    dash: {
      ignoreMinBufferTime: true,
    },
  },
  abr: {
    switchInterval: 2,
    defaultBandwidthEstimate: (1000000), // 10 Mbit/s
    bandwidthDowngradeTarget: 0.4,
    bandwidthUpgradeTarget: 0.2,
  },
  streaming: {
    bufferingGoal: 30,
    rebufferingGoal: 0.1,
    bufferBehind: 0.1,
  },
};

const POLL_INTERVAL = 200;

const PROTECTED_MEDIA = 'https://media.next.openbroadcast.ch/';

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

  constructor() {
    // `audio` is the html5 audio element
    // `player` is the shaka player instance
    const audio = document.createElement('audio');
    const player = new shaka.Player(audio);
    const networkingEngine = player.getNetworkingEngine();
    // set initial configuration & register network filters
    player.configure(SHAKA_CONFIG);
    networkingEngine.registerRequestFilter(requestFilter);

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

    eventBus.on('player:controls', (e) => {
      console.debug('player:controls', e);
      switch (e.do) {
        case 'play': {
          const { url, startTime } = e;
          this.play(url, startTime);
          break;
        }
        case 'seek': {
          const { relPosition } = e;
          // console.debug('seek', relPosition);
          this.seek(relPosition);
          break;
        }
        case 'stop': {
          this.stop();
          break;
        }
        case 'pause': {
          this.pause();
          break;
        }
        case 'resume': {
          this.resume();
          break;
        }
        default: {
          console.debug('unhandled action', e);
          break;
        }
      }
    });

    // eventBus.on('player:controls:playStream', (e) => {
    //   const startTime = (e.startTime) ? e.startTime : -10;
    //   console.debug('player:controls:playStream', startTime);
    // });

    // "audio" events
    // audio.onprogress = (e) => {
    //   console.debug('onprogress', e);
    // };
    audio.onended = (e) => {
      console.debug('AudioPlayer - audio.onended', e);
      eventBus.emit('player:audio:ended', e);
    };
  }

  updateState() {
    const { audio, player } = this;
    const playheadTime = player.getPlayheadTimeAsDate();
    const stats = player.getStats();
    const isLive = player.isLive();
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
      isBuffering: !!(bufferState && bufferState.state === 'buffering'),
      isPlaying: !!(bufferState && bufferState.state === 'playing'),
      isPaused: audio.paused,
      // duration: audio.duration,
      duration: isLive ? null : audio.duration,
      bandwidth,
      currentTime,
      relPosition,
      playheadTime,
    };

    // NOTE: check how to structure playhead info / time...
    if (playheadTime) {
      store.dispatch('time/setPlayheadTime', DateTime.fromJSDate(playheadTime).plus({ seconds: +1 }));
    } else {
      store.dispatch('time/setPlayheadTime', null);
    }

    // if (Object.is(state, this.state)) {
    if (JSON.stringify(playerState) === JSON.stringify(this.playerState)) {
      return;
    }
    // @ts-ignore
    this.playerState = playerState;
    store.dispatch('player/updatePlayerState', { playerState });
  }

  play(url: string, startTime: number = 0) {
    // load url to shaka player, then trigger 'play' on audio element
    this.player.load(url, startTime).then(() => {
      this.audio.play();
    }).catch((e: Error) => {
      console.error(e);
    });
  }

  seek(relPosition: number) {
    if (!(this.playerState && this.playerState.duration)) {
      console.warn('unable to seek');
      return;
    }
    // @ts-ignore
    const absPosition = relPosition * this.playerState.duration;
    this.audio.currentTime = absPosition;
    if (this.playerState.isPaused) {
      this.resume();
    }
  }

  stop() {
    this.player.unload();
    // this.audio.pause();
    // try {
    //   this.audio.currentTime = 0;
    // } catch (err) {
    //   console.warn(err);
    // }
  }

  pause() {
    this.audio.pause();
  }

  resume() {
    this.audio.play();
  }
}

// eslint-disable-next-line import/prefer-default-export
export { AudioPlayer };