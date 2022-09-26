import { computed } from "vue";
import eventBus from "@/eventBus";
import store from "@/store";
import { getMediaUrl } from "@/player/media";
import { playStream } from "@/player/stream";
import createMediaSessionHandler from "@/player/mediaSession";
import type { AudioPlayer } from "@/player/audioPlayer";

createMediaSessionHandler();

const delay = (ms: number) => new Promise((res) => setTimeout(res, ms));

class Queue {
  audioPlayer: AudioPlayer;

  media: any;

  currentMedia: any;

  currentIndex: any;

  previousIndex: any;

  nextIndex: any;

  constructor() {
    this.audioPlayer = window.audioPlayer;
    this.media = computed(() => store.getters["queue/media"]);
    this.currentMedia = computed(() => store.getters["queue/currentMedia"]);
    this.currentIndex = computed(() => store.getters["queue/currentIndex"]);
    this.previousIndex = computed(() => store.getters["queue/previousIndex"]);
    this.nextIndex = computed(() => store.getters["queue/nextIndex"]);

    // 'foreign' events
    eventBus.on("player:audio:ended", async () => {
      console.debug("queue: ended, try to play next");
      try {
        await this.playNext();
      } catch {
        console.info("no next track.. starting live stream");
        playStream();
      }
    });

    // 'queue' events
    eventBus.on("queue:controls:enqueue", async (payload) => {
      // @ts-ignore
      const { media, mode, scope } = { ...payload };
      // console.debug('queue enqueue media', media);
      switch (mode) {
        case "replace": {
          // console.debug('replace');
          await store.dispatch("queue/replaceQueue", { media, scope });
          await this.startPlayCurrent();
          break;
        }
        default: {
          // console.debug('default');
          // check if single mdeia, and if already in queue.
          // if so we start the queue from the media's position instead of replacing.
          if (media.length === 1) {
            // @ts-ignore
            const index = this.media.value.findIndex((obj) => obj.uid === media[0].uid);
            if (index > -1) {
              console.debug("existing single media", index);
              await this.playFromIndex(index);
              return;
            }
          }
          await store.dispatch("queue/replaceQueue", { media, scope });
          await this.startPlayCurrent();
          break;
        }
      }
    });
    eventBus.on("queue:controls:playFromIndex", async (index) => {
      try {
        await this.playFromIndex(index);
      } catch (err) {
        console.warn(err);
      }
    });
    eventBus.on("queue:controls:playNext", async () => {
      try {
        await this.playNext();
      } catch (err) {
        console.warn(err);
      }
    });
    eventBus.on("queue:controls:playPrevious", async () => {
      try {
        await this.playPrevious();
      } catch (err) {
        console.warn(err);
      }
    });
    eventBus.on("queue:controls:startPlayCurrent", async () => {
      try {
        await this.startPlayCurrent();
      } catch (err) {
        console.warn(err);
      }
    });
    eventBus.on("queue:controls:removeAtIndex", async (index) => {
      console.debug("queue:controls:removeAtIndex", index);
      try {
        await this.removeAtIndex(index);
      } catch (err) {
        console.warn(err);
      }
    });
  }

  async playFromIndex(index: number) {
    await store.dispatch("queue/setIndex", index);
    await this.startPlayCurrent();
  }

  // eslint-disable-next-line class-methods-use-this
  async removeAtIndex(index: number) {
    await store.dispatch("queue/removeIndex", index);
  }

  async playPrevious() {
    const previousIndex = this.previousIndex.value;
    if (previousIndex !== null) {
      await store.dispatch("queue/setIndex", previousIndex);
      await this.startPlayCurrent();
    } else {
      throw new Error("no previous media");
    }
  }

  async playNext() {
    const nextIndex = this.nextIndex.value;
    if (nextIndex !== null) {
      // console.debug('queue:playNext', nextIndex)
      await store.dispatch("queue/setIndex", nextIndex);
      // console.debug('queue:playNext - wait 2000ms')
      // await delay(2000);
      // console.debug('queue:playNext - waited 2000ms')
      await this.startPlayCurrent();
      console.debug("queue:playNext - wait 2000ms");
      await delay(2000);
    } else {
      // throw new Error('no next media');
      console.info("no next media - switch to live");
      playStream();
    }
  }

  async startPlayCurrent() {
    // NOTE: not sure if there is no better way.. ;)
    const media = this.currentMedia.value;
    if (!media) {
      console.warn("unable to play: no current media");
      return;
    }
    const url = getMediaUrl(media);
    const { cueIn: startTime, cueOut, fadeIn, fadeOut } = media;
    const endTime = media.duration - cueOut;
    console.debug("queue:startPlayCurrent", {
      startTime,
      endTime,
      fadeIn,
      fadeOut,
      url,
      title: `${media.name} - ${media.artistDisplay}`,
    });
    // console.debug('queue:startPlayCurrent - wait 2000ms')
    // await delay(2000);
    // console.debug('queue:startPlayCurrent - waited 2000ms')
    await this.audioPlayer.play(url, startTime, endTime, fadeIn, fadeOut);
  }
}

export { Queue };
