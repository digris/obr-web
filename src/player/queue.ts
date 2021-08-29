import { computed } from 'vue';
import eventBus from '@/eventBus';
import store from '@/store';
import settings from '@/settings';
import { getMediaUrl } from '@/player/media';
import createMediaSessionHandler from '@/player/mediaSession';

createMediaSessionHandler();

const streamUrl = settings.STREAM_ENDPOINTS.dash;

class Queue {
  media: any;

  currentMedia: any;

  currentIndex: any;

  previousIndex: any;

  nextIndex: any;

  constructor() {
    this.media = computed(() => store.getters['queue/media']);
    this.currentMedia = computed(() => store.getters['queue/currentMedia']);
    this.currentIndex = computed(() => store.getters['queue/currentIndex']);
    this.previousIndex = computed(() => store.getters['queue/previousIndex']);
    this.nextIndex = computed(() => store.getters['queue/nextIndex']);

    // 'foreign' events
    eventBus.on('player:audio:ended', async () => {
      try {
        await this.playNext();
      } catch {
        console.info('no next track.. starting live stream');
        this.startPlayLive();
      }
    });

    // 'queue' events
    eventBus.on('queue:controls:enqueue', async (payload) => {
      // @ts-ignore
      const { media, mode } = { ...payload };
      console.debug('queue:controls:enqueue', mode, media);
      switch (mode) {
        case 'replace': {
          console.debug('replace');
          await store.dispatch('queue/replaceQueue', media);
          await this.startPlayCurrent();
          break;
        }
        default: {
          console.debug('default');
          // check if single mdeia, and if already in queue.
          // if so we start the queue from the media's position instead of replacing.
          if (media.length === 1) {
            // @ts-ignore
            const index = this.media.value.findIndex((obj) => obj.uid === media[0].uid);
            if (index > -1) {
              console.debug('existing single media', index);
              await this.playFromIndex(index);
              return;
            }
          }
          await store.dispatch('queue/replaceQueue', media);
          await this.startPlayCurrent();
          break;
        }
      }
    });
    eventBus.on('queue:controls:playFromIndex', async (index) => {
      try {
        await this.playFromIndex(index);
      } catch (err) {
        console.warn(err);
      }
    });
    eventBus.on('queue:controls:playNext', async () => {
      try {
        await this.playNext();
      } catch (err) {
        console.warn(err);
      }
    });
    eventBus.on('queue:controls:playPrevious', async () => {
      try {
        await this.playPrevious();
      } catch (err) {
        console.warn(err);
      }
    });
    eventBus.on('queue:controls:startPlayCurrent', async () => {
      try {
        await this.startPlayCurrent();
      } catch (err) {
        console.warn(err);
      }
    });
    eventBus.on('queue:controls:removeAtIndex', async (index) => {
      console.debug('queue:controls:removeAtIndex', index);
      try {
        await this.removeAtIndex(index);
      } catch (err) {
        console.warn(err);
      }
    });
  }

  async playFromIndex(index: number) {
    await store.dispatch('queue/setIndex', index);
    this.startPlayCurrent();
  }

  // eslint-disable-next-line class-methods-use-this
  async removeAtIndex(index: number) {
    await store.dispatch('queue/removeIndex', index);
  }

  async playPrevious() {
    const previousIndex = this.previousIndex.value;
    if (previousIndex !== null) {
      await store.dispatch('queue/setIndex', previousIndex);
      this.startPlayCurrent();
    } else {
      throw new Error('no previous media');
    }
  }

  async playNext() {
    const nextIndex = this.nextIndex.value;
    if (nextIndex !== null) {
      await store.dispatch('queue/setIndex', nextIndex);
      this.startPlayCurrent();
    } else {
      // throw new Error('no next media');
      console.info('no next media - switch to live');
      this.startPlayLive();
    }
  }

  startPlayCurrent() {
    // NOTE: not sure if there is no better way.. ;)
    const media = this.currentMedia.value;
    const url = getMediaUrl(media);
    const event = {
      do: 'play',
      url,
      startTime: 0,
    };
    eventBus.emit('player:controls', event);
  }

  // eslint-disable-next-line class-methods-use-this
  startPlayLive() {
    // NOTE: not sure if there is no better way.. ;)
    const event = {
      do: 'play',
      url: `${streamUrl}?${Date.now()}`,
      startTime: -10,
    };
    eventBus.emit('player:controls', event);
  }
}

const queue = new Queue();

export default queue;
