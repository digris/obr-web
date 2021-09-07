import store from '@/store';
import eventBus from '@/eventBus';
import { getImageSrc } from '@/utils/image';

class MediaSessionHandler {
  session: null;

  constructor() {
    if ('mediaSession' in navigator) {
      // @ts-ignore
      this.session = navigator.mediaSession;
      this.setupBindings(true);
      store.watch((state: any, getters: any) => {
        return getters['player/media'];
      }, (media) => {
        // console.debug('player/media', media);
        this.setMetadata(media);
        const isLive = store.getters['player/isLive'];
        // console.debug('player/isLive', isLive);
        this.setupBindings(isLive);
      });
    }
  }

  setupBindings(isLive: boolean) {
    // @ts-ignore
    this.session.setActionHandler('pause', () => {
      eventBus.emit('player:controls', { do: 'pause' });
    });
    if (isLive) {
      // @ts-ignore
      this.session.setActionHandler('previoustrack', null);
      // @ts-ignore
      this.session.setActionHandler('nexttrack', null);
    } else {
      // @ts-ignore
      this.session.setActionHandler('previoustrack', () => {
        eventBus.emit('queue:controls:playPrevious');
      });
      // @ts-ignore
      this.session.setActionHandler('nexttrack', () => {
        eventBus.emit('queue:controls:playNext');
      });
    }
  }

  setMetadata(media: any) {
    const release = (media.releases.length) ? media.releases[0] : null;
    const artwork: { src: string | null; sizes: string; type: string; }[] = [];
    if (release && release.image) {
      const sizes = [96, 256];
      sizes.forEach((size) => {
        artwork.push({
          src: getImageSrc(release.image, size),
          sizes: `${size}x${size}`,
          type: 'image/png',
        });
      });
    }
    // @ts-ignore
    this.session.metadata = new MediaMetadata({
      title: media.name,
      artist: media.artistDisplay,
      album: (release) ? release.name : '-',
      artwork,
    });
  }
}

export default function () {
  return new MediaSessionHandler();
}
