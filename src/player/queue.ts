import eventBus from '@/eventBus';
import store from '@/store';
import settings from '@/settings';
import { computed } from 'vue';
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
      throw new Error('no next media');
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

// eslint-disable-next-line import/prefer-default-export
export { Queue };
