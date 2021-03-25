<script>
import shaka from 'shaka-player';

export default {
  name: 'Player',
  props: {
    msg: String,
    // player: null,
  },
  computed: {
    liveUrl() {
      // return `http://localhost:7777/data/stream.mpd?${Date.now()}`;
      return `https://stream-abr.next.openbroadcast.ch/stream.mpd?${Date.now()}`;
      // return 'https://obr-stream.hazelfire.com/256.mp3';
      // return 'http://10.59.0.100:7777/data/stream.mpd';
      // return 'https://storage.googleapis.com/shaka-demo-assets/angel-one/dash.mpd';
    },
    onDemandUrl() {
      // return 'http://localhost:7777/data/_encoded/F001/manifest.mpd';
      // return 'https://media.next.openbroadcast.ch/encoded/F003/manifest.mpd';
      return 'https://media.next.openbroadcast.ch/encoded/_encoded/F003/manifest.mpd';
      // return 'http://next.openbroadcast.ch:8080/catalog/media/manifest/F001/';
    },
    onDemandUrl2() {
      // return 'https://media.next.openbroadcast.ch/encoded/F002/manifest.mpd';
      // return 'http://mbp15.local:7777/data/_encoded/F002/manifest.mpd';
      return 'https://media.next.openbroadcast.ch/encoded/F002/manifest.mpd';
      // return 'http://mbp15.local:7777/data/_hls/F002/master.m3u8';
    },
    configuration() {
      return this.$store.getters['player/configuration'];
    },
    bufferInfo() {
      return this.$store.getters['player/bufferInfo'];
    },
    currentState() {
      return this.$store.getters['player/currentState'];
    },
    playhead() {
      return this.$store.getters['player/playhead'];
    },
  },
  mounted() {
    const audio = this.$refs.audioPlayer;
    const player = new shaka.Player(audio);
    window.audio = audio;
    window.player = player;
    // const licenseServer = 'https://cwip-shaka-proxy.appspot.com/cookie_auth';
    player.configure({
      // drm: {
      //   servers: { 'com.widevine.alpha': licenseServer },
      // },
      manifest: {
        dash: {
          ignoreMinBufferTime: true,
        },
      },
      abr: {
        switchInterval: 1,
        defaultBandwidthEstimate: (1000000), // 10 Mbit/s
        bandwidthDowngradeTarget: 0.8,
        bandwidthUpgradeTarget: 0.6,
      },
      streaming: {
        // bufferingGoal: 30,
        bufferingGoal: 30,
        rebufferingGoal: 0.1,
        bufferBehind: 0.1,
      },
    });

    player.getNetworkingEngine().registerRequestFilter((type, request) => {
      const protectedBase = 'https://media.next.openbroadcast.ch/';
      if (request.uris.findIndex((uri) => uri.startsWith(protectedBase)) === 0) {
        console.debug('protectedBase', protectedBase);
        /* eslint-disable-next-line no-param-reassign */
        request.allowCrossSiteCredentials = true;
      }
    });
    //
    audio.addEventListener('ended', () => {
      this.play(this.liveUrl, -10);
    });

    // console.debug(player.getConfiguration());
    this.$store.dispatch('player/updateConfiguration', { configuration: player.getConfiguration() });
    this.player = player;
    this.audio = audio;
    setInterval(() => {
      this.$store.dispatch('player/updateConfiguration', { configuration: player.getConfiguration() });
    }, 5000);
    setInterval(() => {
      this.$store.dispatch('player/updatePlayer', { player });
    }, 50);
  },
  methods: {
    play(url, startTime) {
      this.player.load(url, startTime)
        .then(() => {
          this.$refs.audioPlayer.play();
        })
        .catch(this.onError);
    },
    onError(e) {
      /* eslint-disable-next-line no-console */
      console.error(e);
    },
  },
};
</script>

<template>
  <div class="hello">
    <div ref="audioContainer">
      <div>
        <button @click="play(liveUrl, -10)">LIVE</button>
        <button @click="play(onDemandUrl)">ON DEMAND</button>
        <button @click="play(onDemandUrl2, 0)">ON DEMAND 2</button>
      </div>
      <audio
        id="audio"
        ref="audioPlayer"
        controls="controls"
      ></audio>
    </div>
    <pre
      v-text="playhead"
      class="debug"
    />
    <pre
      v-if="currentState"
      v-text="currentState.state"
      class="debug"
    />
    <pre
      v-if="(1 === 2)"
      v-text="bufferInfo"
      class="debug"
    />
  </div>
</template>

<style scoped>
.hello {
  background: #f00;
}
h3 {
  margin: 40px 0 0;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #fff;
}
</style>
